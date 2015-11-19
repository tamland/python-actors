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
        return isinstance(other, ActorRef) and other._cell is self._cell


class InternalRef(ActorRef):

    def __init__(self, cell):
        super(InternalRef, self).__init__(cell)

    def send_system_message(self, message):
        self._cell.send_system_message(message)
