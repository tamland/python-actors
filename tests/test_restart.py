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
