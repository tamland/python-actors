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
        mailbox.close()

    def schedule_execution(self, mailbox):
        if mailbox.is_closed() or mailbox.is_scheduled() or not mailbox.has_messages():
            return

        if mailbox.set_scheduled():
            self._executor.submit(mailbox.process_messages)

    def await_shutdown(self):
        if self._attached_count > 0:
            self._terminated.future.get()
        self._executor.shutdown()


class PinnedDispatcher(Dispatcher):

    def __init__(self):
        super(PinnedDispatcher, self).__init__(Executor(1))
