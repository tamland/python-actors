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

from actors.ref import ActorRef
from actors.utils.ask import ask, PromiseActorRef
from .mock_compat import Mock


def test_ask_forwards_message_with_promise_actor_as_sender():
    actor = Mock(spec=ActorRef)
    message = object()
    ask(actor, message)

    assert actor.tell.call_count == 1
    assert actor.tell.call_args[0][0] is message
    assert isinstance(actor.tell.call_args[0][1], PromiseActorRef)


def test_tell_completes_future():
    actor = PromiseActorRef()
    actor.promise = Mock()
    message = object()
    actor.tell(message)

    actor.promise.complete.assert_called_once_with(message)
