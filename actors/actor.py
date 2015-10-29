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
