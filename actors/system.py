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

from actors.actor import Actor
from actors.cell import ActorCell
from actors.dispatch.event_based import EventBasedDispatcher


class ActorSystem(object):
    default_dispatcher = EventBasedDispatcher()

    future_executor = None

    def __init__(self):
        self._actors = []

    def actor_of(self, cls, dispatcher=None):
        actor = cls()
        assert isinstance(actor, Actor)

        if dispatcher is None:
            dispatcher = self.default_dispatcher

        cell = ActorCell(
            actor,
            system=self,
            dispatcher=dispatcher,
        )
        dispatcher.attach(cell)

        self._actors.append(cell)

        return cell.ref

    def stop(self):
        for actor in self._actors:
            actor.stop()
            pass
