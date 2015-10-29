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
from actors.internal.messages import Restart, Start
from .mock_compat import Mock


@pytest.fixture
def actor():
    return Mock(spec_set=Actor)


@pytest.fixture
def factory(actor):
    return Mock(return_value=actor)


@pytest.fixture
def cell(factory):
    cell = Cell(factory, Mock(), Mock(), Mock())
    cell.handle_system_message(Start)
    return cell


def test_restart_constructs_new_instance(factory, cell):
    assert factory.call_count == 1
    cell.handle_system_message(Restart)
    assert factory.call_count == 2


def test_restart_calls_pre_restart_on_old_and_post_on_new():
    actor1 = Mock(spec_set=Actor)
    actor2 = Mock(spec_set=Actor)

    it = iter([actor1, actor2])

    cell = Cell(lambda: next(it), Mock(), Mock(), Mock())
    cell.handle_system_message(Start)

    cell.handle_system_message(Restart)
    actor1.pre_restart.assert_called_once_with()
    actor2.post_restart.assert_called_once_with()


def test_failure_in_restart_hooks_should_stop_actor():
    pass
