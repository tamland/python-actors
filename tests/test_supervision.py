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
from actors.internal.cell import Cell
from actors.internal.messages import Resume, Failure, Start, Restart
from actors.ref import InternalRef
from .mock_compat import Mock


@pytest.fixture
def actor():
    actor = Mock(spec=Actor)
    actor.__class__ = Mock()
    actor.__class__.supervisor_strategy.return_value = Resume
    return actor


@pytest.fixture
def cell(actor):
    cell = Cell(lambda: actor, Mock(), Mock(), Mock())
    cell.handle_system_message(Start)
    return cell


def test_supervisor_should_ask_actor_class_for_strategy(actor, cell):
    cell.handle_system_message(Failure(Mock(), Mock(), Mock()))
    assert not actor.supervisor_strategy.called
    assert actor.__class__.supervisor_strategy.called


def test_supervisor_should_direct_child_on_failure(actor, cell):
    actor.__class__.supervisor_strategy.return_value = Restart
    child = Mock(spec=InternalRef)
    cell.handle_system_message(Failure(child, ValueError(), ""))
    child.send_system_message.assert_called_once_with(Restart)

