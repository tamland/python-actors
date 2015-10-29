# -*- coding: utf-8 -*-
#
# Copyright 2015 Thomas Amland
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import deque
from threading import Lock


class _Status(object):
    OPEN = object()
    CLOSED = object()
    SUSPENDED = object()


class _ScheduleState(object):
    IDLE = 1
    SCHEDULED = 2


class InternalMailbox(object):
    def __init__(self, dispatcher, actor, throughput=5):
        # Should only be set in message handler
        self._primary_status = _Status.OPEN

        self._idle = _ScheduleState.IDLE
        self._idle_lock = Lock()

        self._message_queue = deque()
        self._system_message_queue = deque()
        self._actor = actor
        self._dispatcher = dispatcher
        self._throughput = throughput

    def enqueue(self, item):
        self._message_queue.append(item)

    def enqueue_system(self, item):
        self._system_message_queue.append(item)

    def close(self):
        """ Stop processing of all messages."""
        self._primary_status = _Status.CLOSED

    def suspend(self):
        """ Stop processing of user message. """
        self._primary_status = _Status.SUSPENDED

    def resume(self):
        """ Continue processing of user message. """
        self._primary_status = _Status.OPEN

    def is_closed(self):
        return self._primary_status is _Status.CLOSED

    def is_suspended(self):
        return self._primary_status is _Status.SUSPENDED

    def has_messages(self):
        return len(self._message_queue) > 0 or len(self._system_message_queue) > 0

    def is_idle(self):
        return self._idle

    def is_scheduled(self):
        return not self._idle

    def set_scheduled(self):
        """
        Returns True if state was successfully changed from idle to scheduled.
        """
        with self._idle_lock:
            if self._idle:
                self._idle = False
                return True
        return False

    def set_idle(self):
        with self._idle_lock:
            self._idle = True

    def process_messages(self):
        if self._primary_status is _Status.CLOSED or not self.has_messages():
            return

        self._process_system_message()

        if self._primary_status is _Status.OPEN:
            for _ in range(min(self._throughput, len(self._message_queue))):
                self._actor.handle_message(self._message_queue.popleft())
                self._process_system_message()
                if self._primary_status is not _Status.OPEN:
                    break

        self.set_idle()
        self._dispatcher.schedule_execution(self)

    def _process_system_message(self):
        if len(self._system_message_queue) > 0:
            self._actor.handle_system_message(self._system_message_queue.popleft())

    def flush_messages(self):
        if not self.is_closed():
            raise Exception()

        messages = []
        while len(self._message_queue) > 0:
            messages.append(self._message_queue.popleft())
        return messages
