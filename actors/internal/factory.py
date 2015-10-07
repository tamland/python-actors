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
            dispatcher = self._system.default_dispatcher

        from actors.internal.cell import Cell
        cell = Cell(factory, dispatcher=dispatcher, system=self._system,
                         parent=self._supervisor)

        internal_ref = InternalRef(cell)
        self._supervisor.send_system_message(Supervise(internal_ref))
        internal_ref.send_system_message(Start)

        return ActorRef(cell)
