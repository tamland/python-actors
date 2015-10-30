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

import pytest
from actors.actor import Actor
from actors.internal.factory import ActorFactory
from actors.internal.messages import Supervise
from actors.ref import InternalRef, ActorRef
from actors.system import ActorSystem
from actors.utils.ask import ask, PromiseActorRef
from ..mock_compat import Mock


@pytest.fixture
def supervisor():
    return Mock(spec_set=InternalRef)


@pytest.fixture
def factory(supervisor):
    return ActorFactory(Mock(), supervisor)


def test_child_adds_itself_to_parent(supervisor, factory):
    factory.actor_of(Mock())
    assert supervisor.send_system_message.called
    assert type(supervisor.send_system_message.call_args[0][0]) is Supervise


def test_ask():
    class Test(Actor):
        def receive(self, message):
            self.context.sender.tell(message)

    with ActorSystem() as system:
        actor = system.actor_of(Test)
        message = object()
        reply = ask(actor, message)
        assert reply.get(timeout=1) is message


def test_calling_tell_on_promise_actor_completes_future():
    actor = PromiseActorRef()
    actor.promise = Mock()
    message = object()
    actor.tell(message)

    actor.promise.complete.assert_called_once_with(message)


def test_ask_forwards_message_with_promise_actor_as_sender():
    actor = Mock(spec=ActorRef)
    message = object()
    ask(actor, message)

    assert actor.tell.call_count == 1
    assert actor.tell.call_args[0][0] is message
    assert isinstance(actor.tell.call_args[0][1], PromiseActorRef)
