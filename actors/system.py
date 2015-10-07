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

import logging
import actors.internal.cell
import actors.internal.factory
from actors.future import Promise
from actors.ref import ActorRef, InternalRef
from actors.actor import Actor
from actors.internal.dispatcher import Dispatcher
from actors.internal.messages import Terminate, Start, DeadLetter
from actors.internal.executor import Executor


class ActorSystem(actors.internal.factory.ActorFactory):

    def __init__(self):
        self.default_dispatcher = Dispatcher(Executor())
        self._dead_letters = _DeadLetterRef()
        self._terminate_promise = Promise()
        self._init_guardian()
        actors.internal.factory.ActorFactory.__init__(self, self, self._guardian)

    def _init_guardian(self):
        class Empty(Actor):
            def receive(self, message):
                pass

            def post_stop(self):
                pass

        cell = actors.internal.cell.Cell(Empty, dispatcher=self.default_dispatcher,
                                         system=self, parent=None)
        self._guardian = InternalRef(cell)
        self._guardian.send_system_message(Start)

    def terminate(self):
        self._guardian.send_system_message(Terminate)
        self.default_dispatcher.await_shutdown()

    @property
    def dead_letters(self):
        return self._dead_letters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()


class Guardian(Actor):
    def __init__(self):
        super(Guardian, self).__init__()

    def receive(self, message):
        assert False, "Should not be called"


class _DeadLetterRef(ActorRef):
    def __init__(self):
        super(_DeadLetterRef, self).__init__(None)
        self._logger = logging.getLogger('dead letter')

    def tell(self, message, sender=None):
        if isinstance(message, DeadLetter):
            self._logger.debug("Message %r from %r to %r was not delivered.",
                message.message, message.sender, message.recipient)
        else:
            self._logger.debug("Message %r from %r was not delivered.")
