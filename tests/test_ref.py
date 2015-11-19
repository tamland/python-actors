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
from actors.internal.cell import Cell
from actors.ref import ActorRef, InternalRef
from .mock_compat import Mock


def test_tell_sends_message_and_sender_to_cell():
    cell = Mock(spec_set=Cell)
    sender = Mock(spec_set=ActorRef)
    message = object()
    ref = ActorRef(cell)
    ref.tell(message, sender)

    cell.send_message.assert_called_once_with(message, sender)


def test_tell_raises_if_sender_is_not_an_actor_ref():
    ref = ActorRef(Mock())
    with pytest.raises(ValueError):
        ref.tell(Mock(), object())


def test_equality():
    cell_1 = object()
    cell_2 = object()
    assert ActorRef(cell_1) != ActorRef(cell_2)
    assert ActorRef(cell_1) == ActorRef(cell_1)
    assert InternalRef(cell_1) != InternalRef(cell_2)
    assert InternalRef(cell_1) == InternalRef(cell_1)
    assert InternalRef(cell_1) == ActorRef(cell_1)
    assert ActorRef(cell_1) != object()


