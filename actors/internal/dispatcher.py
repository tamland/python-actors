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

from threading import Lock
from actors.internal.executor import Executor
from actors.future import Promise


class Dispatcher(object):
    throughput = 5

    def __init__(self, executor):
        self._executor = executor
        self._attach_lock = Lock()
        self._attached_count = 0
        self._terminated = Promise()

    def dispatch(self, message, mailbox):
        if not mailbox.is_closed():
            mailbox.enqueue(message)
            self.schedule_execution(mailbox)
        else:
            print("Failed to deliver message. mailbox closed")

    def dispatch_system(self, message, mailbox):
        if not mailbox.is_closed():
            mailbox.enqueue_system(message)
            self.schedule_execution(mailbox)
        else:
            print("Failed to deliver system message. mailbox closed")

    def attach(self, mailbox):
        with self._attach_lock:
            self._attached_count += 1
        assert not mailbox.is_closed()

    def detach(self, mailbox):
        assert mailbox.is_closed()
        with self._attach_lock:
            self._attached_count -= 1
            if self._attached_count == 0:
                self._terminated.complete(None)
                self._executor.shutdown()

    def schedule_execution(self, mailbox):
        if mailbox.is_closed() or mailbox.is_scheduled() or not mailbox.has_messages():
            return

        if mailbox.set_scheduled():
            self._executor.submit(mailbox.process_messages)


class PinnedDispatcher(Dispatcher):

    def __init__(self):
        super(PinnedDispatcher, self).__init__(Executor(1))
