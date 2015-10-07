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
from actors import Actor, ActorSystem, Envelope
from actors.internal.cell import Cell
from actors.internal.dispatcher import Dispatcher
from actors.internal.mailbox import InternalMailbox
from actors.internal.messages import Start, Terminate, Supervise, DeadLetter
from actors.ref import InternalRef, ActorRef
from .mock_compat import Mock, MagicMock


@pytest.fixture
def actor():
    return Mock(spec_set=Actor)


@pytest.fixture
def supervisor():
    return Mock(spec_set=Cell)


@pytest.fixture
def dispatcher():
    return Mock(spec_set=Dispatcher)


@pytest.fixture
def mailbox():
    return MagicMock(spec_set=InternalMailbox)


@pytest.fixture
def system():
    return MagicMock(spec_set=ActorSystem)


@pytest.fixture
def cell(actor, system, dispatcher, supervisor, mailbox):
    cell = Cell(lambda: actor, system, dispatcher, supervisor)
    cell._mailbox = mailbox
    cell.handle_system_message(Start)
    return cell


def test_terminate_calls_stop_hook(actor, cell):
    cell.handle_system_message(Terminate)
    actor.post_stop.assert_called_once_with()


def test_terminate_closes_mailbox(cell, mailbox):
    cell.handle_system_message(Terminate)
    mailbox.close.assert_called_once_with()


def test_terminate_flush_mailbox(cell, mailbox):
    cell.handle_system_message(Terminate)
    mailbox.flush_messages.assert_called_once_with()


def test_terminate_sender_unhandled_messages_to_dead_letters(cell, mailbox, system):
    message = Mock()
    sender = Mock()
    mailbox.flush_messages.return_value = [Envelope(message, sender)]
    cell.handle_system_message(Terminate)
    system.dead_letters.tell.assert_called_once_with(DeadLetter(
        message, sender, ActorRef(cell)))


def test_terminate_detach_actor_from_dispatcher(cell, mailbox, dispatcher):
    cell.handle_system_message(Terminate)
    dispatcher.detach.assert_called_once_with(mailbox)


def test_terminate_sends_terminate_message_to_children(cell):
    child = Mock(spec_set=InternalRef)
    cell.handle_system_message(Supervise(child))
    cell.handle_system_message(Terminate)
    child.send_system_message.assert_called_once_with(Terminate)


def test_sending_message_to_terminated_actor_should_forward_to_dead_letters(cell, system):
    cell.handle_system_message(Terminate)
    message = Mock()
    sender = Mock()
    cell.send_message(message, sender)
    system.dead_letters.tell.assert_called_once_with(DeadLetter(
        message, sender, ActorRef(cell)))


