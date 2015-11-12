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
from actors.internal.factory import ActorFactory
from actors.internal.messages import Supervise
from actors.ref import InternalRef
from tests.mock_compat import Mock


def test_actor_of_send_supervise_message_to_parent_on_creation():
    supervisor = Mock(spec_set=InternalRef)
    factory = ActorFactory(Mock(), supervisor)
    factory.actor_of(Mock())
    assert supervisor.send_system_message.called
    assert type(supervisor.send_system_message.call_args[0][0]) is Supervise


def test_actor_of_raise_if_factory_or_behavior_is_not_provider():
    factory = ActorFactory(Mock(), Mock())
    with pytest.raises(ValueError):
        factory.actor_of()
