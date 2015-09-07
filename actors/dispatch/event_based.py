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

from functools import partial
from collections import deque
from threading import Lock
from six.moves import range
from actors.dispatch.dispatcher import Dispatcher
from actors.dispatch.mailbox import Mailbox
from actors.dispatch.executor import Executor


class State(object):
    WAITING = 1
    WORKING = 2


class MailboxImpl(Mailbox):
    def __init__(self):
        super(MailboxImpl, self).__init__()
        self.state = State.WAITING
        self.state_lock = Lock()
        self._queue = deque()

    def enqueue(self, item):
        self._queue.append(item)

    def dequeue(self):
        return self._queue.popleft()

    def __len__(self):
        return len(self._queue)

    def set_scheduled(self):
        with self.state_lock:
            if self.state == State.WAITING:
                self.state = State.WORKING
                return True
        return False

    def set_idle(self):
        with self.state_lock:
            self.state = State.WAITING


class EventBasedDispatcher(Dispatcher):
    throughput = 5

    def __init__(self):
        super(EventBasedDispatcher, self).__init__()
        self._executor = Executor()

    def create_mailbox(self):
        return MailboxImpl()

    def dispatch(self, envelope, actor):
        actor.mailbox.enqueue(envelope)
        self._schedule(actor)

    def attach(self, actor):
        assert isinstance(actor.mailbox, Mailbox)
        actor.mailbox.open()

    def detach(self, actor):
        actor.mailbox.close()

    def _schedule(self, actor):
        if len(actor.mailbox) == 0:
            return

        if actor.mailbox.state == State.WORKING:
            return

        if actor.mailbox.set_scheduled():
            self._executor.submit(partial(self._process_mailbox, actor))

    def _process_mailbox(self, actor):
        for _ in range(self.throughput):
            envelope = actor.mailbox.dequeue()
            actor.process_message(envelope)
            if len(actor.mailbox) == 0:
                break
            if actor.mailbox.closed:
                break

        actor.mailbox.set_idle()

        if not actor.mailbox.closed:
            self._schedule(actor)

    def shutdown(self):
        # self._executor.shutdown()
        pass
