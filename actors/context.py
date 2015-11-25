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

    :ivar system: The system  this actor belongs to.
    :vartype system: :class:`ActorSystem`
    """

    sender = None
    self_ref = None
    parent = None
    system = None

    def stop(self):
        self.self_ref.send_system_message(Terminate)
