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

import time
from actors.actor import Actor
from actors.system import ActorSystem
from actors.utils.ask import ask
from ..mock_compat import Mock


def test_system():
    class Test(Actor):
        def receive(self, message):
            self.context.sender.tell(message)

    with ActorSystem() as system:
        actor = system.actor_of(Test)
        message = object()
        reply = ask(actor, message)
        assert reply.get(timeout=10) is message


def test_behaviour():
    with ActorSystem() as system:
        behaviour = Mock()
        actor = system.actor_of(behaviour=behaviour)
        message = object()
        actor.tell(message)
        time.sleep(1)
        behaviour.assert_called_once_with(message)
