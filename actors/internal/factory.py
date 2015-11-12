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

import actors.actor
from actors.internal.messages import Start, Supervise
from actors.ref import ActorRef, InternalRef


def _actor_from_behaviour(behaviour):
    class Wrapper(actors.actor.Actor):
        def receive(self, message):
            behaviour(message)
    return Wrapper


class ActorFactory(object):

    def __init__(self, system, supervisor):
        """
        :param system:
        :type system: :class:`ActorSystem`

        :param supervisor:
        :type supervisor: :class:`InternalRef`
        """
        self._system = system
        self._supervisor = supervisor

    def actor_of(self, cls=None, behaviour=None, dispatcher=None):
        if cls:
            factory = cls
        elif behaviour:
            factory = _actor_from_behaviour(behaviour)
        else:
            raise ValueError()

        if dispatcher is None:
            dispatcher = self._system._system_dispatcher

        from actors.internal.cell import Cell
        cell = Cell(factory, dispatcher=dispatcher, system=self._system,
                         parent=self._supervisor)

        internal_ref = InternalRef(cell)
        self._supervisor.send_system_message(Supervise(internal_ref))
        internal_ref.send_system_message(Start)

        return ActorRef(cell)
