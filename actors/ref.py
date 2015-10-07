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

from . import no_sender


class ActorRef(object):
    __slots__ = ('_cell',)

    def __init__(self, _cell):
        self._cell = _cell

    def tell(self, message, sender=no_sender):
        """ Send a message to this actor. Asynchronous fire-and-forget.

        :param message: The message to send.
        :type message: Any

        :param sender: The sender of the message. If provided it will be made
            available to the receiving actor via the :attr:`Actor.sender` attribute.
        :type sender: :class:`Actor`
        """
        if sender is not no_sender and not isinstance(sender, ActorRef):
            raise ValueError("Sender must be actor reference")

        self._cell.send_message(message, sender)

    def __eq__(self, other):
        return self._cell is other._cell


class InternalRef(object):
    __slots__ = ('_cell',)

    def __init__(self, cell):
        self._cell = cell

    def send_system_message(self, message):
        self._cell.send_system_message(message)
