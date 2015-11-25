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

    def __init__(self, system_dispatcher=None):
        """
        The actor system is responsible for creating, configuring and stopping actors and
        dispatchers.

        Normally, only one system per application should be created.

        :param system_dispatcher: Override the dispatcher used by the system. This also acts as the
            default dispatcher for new actors.
        :type system_dispatcher: :class:`Dispatcher`
        """
        self._system_dispatcher = Dispatcher(Executor()) \
            if system_dispatcher is None else system_dispatcher
        self._dead_letters = _DeadLetterRef()

        self._terminate_promise = Promise()

        class Guardian(Actor):
            def __init__(me):
                me._logger = logging.getLogger(__name__)

            def receive(me, message):
                me._logger.warning("User receive called. This should not be happen.")

            def post_stop(me):
                self._terminate_promise.complete(None)

        self._guardian = InternalRef(actors.internal.cell.Cell(Guardian,
            dispatcher=self._system_dispatcher, system=self, parent=None))
        self._guardian.send_system_message(Start)

        actors.internal.factory.ActorFactory.__init__(self, self, self._guardian)

    def terminate(self):
        self._guardian.send_system_message(Terminate)
        self._terminate_promise.future.get()

    @property
    def dead_letters(self):
        return self._dead_letters

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()


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
