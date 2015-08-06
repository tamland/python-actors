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
import threading
from six.moves import queue
from actors.dispatch.dispatcher import Dispatcher
from actors.dispatch.mailbox import Mailbox


class BlockingMailbox(Mailbox):
    def __init__(self):
        super(BlockingMailbox, self).__init__()
        self.queue = queue.Queue()


class BlockingDispatcher(Dispatcher):
    _INTERRUPT = object()

    def __init__(self):
        super(BlockingDispatcher, self).__init__()
        self._thread = None

    def create_mailbox(self):
        return BlockingMailbox()

    def dispatch(self, envelope, actor):
        try:
            actor.mailbox.queue.put_nowait(envelope)
        except queue.QueueFull as e:
            # TODO
            raise e

    def attach(self, actor):
        assert isinstance(actor.mailbox, BlockingMailbox)
        actor.mailbox.actor = actor

        assert self._thread is None, "Can't reattach"
        self._thread = threading.Thread(
            target=partial(self._process_mailbox, actor))
        self._thread.start()

    def detach(self, actor):
        actor.mailbox.close()
        assert actor.mailbox.closed
        actor.mailbox.actor = None
        actor.mailbox.queue.put(self._INTERRUPT)
        self._thread.join()

    def _process_mailbox(self, actor):
        while True:
            envelope = actor.mailbox.queue.get(block=True)
            if actor.mailbox.closed:
                break
            assert envelope is not self._INTERRUPT
            actor.process_message(envelope)


