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

from . import default_supervisor_strategy


class Actor(object):
    """ The base class implemented by all actors.

    :ivar context: Provides contextual information about this actor and the
        current message. Only valid within this actor.
    :vartype context: :class:`ActorContext`

    """

    context = None

    supervisor_strategy = default_supervisor_strategy
    """ Class method. Override to provide custom supervisor behaviour for this actor. """

    def receive(self, message):
        """
        Override to provide the actor behaviour.

        :param message: The current message.
        """

    def pre_start(self):
        """ Called asynchronous before processing any messages. """

    def post_stop(self):
        """ Called asynchronous after the actor has stopped. """

    def pre_restart(self):
        """ Called on the failed actor before it's disposed of. """

    def post_restart(self):
        """ Called on the newly created actor. """

    @property
    def sender(self):
        """ Alias for :attr:`self.context.sender`. """
        return self.context.sender

    @property
    def ref(self):
        """ Alias for :attr:`self.context.self_ref`. """
        return self.context.self_ref
