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

from actors import ActorRef
from actors.utils.proxy import ProxyActor, ProxyRef, Invoke
from .mock_compat import Mock


def test_invoking_method_on_ref_sends_invoke_message():
    underlying = Mock(spec_set=ActorRef)
    ref = ProxyRef(underlying)
    ref.foo(1, 2, bar=3)
    underlying.tell.assert_called_once_with(Invoke('foo', (1, 2), {'bar': 3}))


def test_sending_invoke_message_calls_method():
    actor = ProxyActor()
    actor.foo = Mock()
    actor.receive(Invoke('foo', (1, 2), {'bar': 3}))
    actor.foo.assert_called_once_with(1, 2, bar=3)
