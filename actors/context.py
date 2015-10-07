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

import actors.internal.factory
from actors.internal.messages import Terminate


class ActorContext(actors.internal.factory.ActorFactory):
    """
    Provides contextual information to actors. Only valid within the
    :meth:`Actor.receive` method.

    :ivar sender: The sender of the current message.
    :vartype sender: :class:`ActorRef`

    :ivar self_ref: An :class:`ActorRef` to the this actor.
    :vartype self_ref: :class:`ActorRef`

    :ivar parent: The parent of this actor.
    :vartype parent: :class:`ActorRef`
    """

    sender = None
    self_ref = None
    parent = None

    def stop(self):
        self.self_ref.send_system_message(Terminate)
