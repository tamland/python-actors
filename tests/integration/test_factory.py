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

import pytest
from actors.actor import Actor
from actors.internal.factory import ActorFactory
from actors.internal.messages import Supervise
from actors.ref import InternalRef, ActorRef
from actors.system import ActorSystem
from actors.utils import ask, PromiseActorRef
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
