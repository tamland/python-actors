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


