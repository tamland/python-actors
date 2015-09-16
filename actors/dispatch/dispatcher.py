# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 Thomas Amland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals
from collections import deque
from threading import Lock
from actors.dispatch.executor import Executor


class State(object):
    WAITING = 1
    WORKING = 2


class Dispatcher(object):
    throughput = 5

    def __init__(self):
        super(Dispatcher, self).__init__()
        self._executor = Executor()

    def create_mailbox(self):
        return InternalMailbox(self)

    def dispatch(self, envelope, actor):
        actor.mailbox.enqueue(envelope)
        self.schedule_execution(actor.mailbox)

    def attach(self, actor):
        assert isinstance(actor.mailbox, InternalMailbox)
        actor.mailbox.set_actor(actor)
        actor.mailbox.open()

    def detach(self, actor):
        actor.mailbox.close()

    def schedule_execution(self, mailbox):
        if len(mailbox) == 0:
            return

        if mailbox.state == State.WORKING:
            return

        if mailbox.set_scheduled():
            self._executor.submit(mailbox.process_mailbox)

    def shutdown(self):
        self._executor.shutdown()


class InternalMailbox(object):
    def __init__(self, dispatcher):
        super(InternalMailbox, self).__init__()
        self.closed = True
        self.state = State.WAITING
        self.state_lock = Lock()
        self._queue = deque()
        self._actor = None
        self._dispatcher = dispatcher

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        return self._queue.popleft()

    def __len__(self):
        return len(self._queue)

    def open(self):
        self.closed = False

    def close(self):
        self.closed = True

    def set_scheduled(self):
        with self.state_lock:
            if self.state == State.WAITING:
                self.state = State.WORKING
                return True
        return False

    def set_idle(self):
        with self.state_lock:
            self.state = State.WAITING

    def set_actor(self, actor):
        self._actor = actor

    def process_mailbox(self):
        for _ in range(self._dispatcher.throughput):
            envelope = self.dequeue()
            self._actor.process_message(envelope)
            if len(self._queue) == 0:
                break
            if self.closed:
                break

        self.set_idle()

        if not self.closed:
            self._dispatcher.schedule_execution(self)