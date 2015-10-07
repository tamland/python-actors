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

