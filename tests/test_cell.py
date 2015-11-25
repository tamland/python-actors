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
from actors.ref import ActorRef
from .mock_compat import Mock
from actors import Envelope, ActorInitializationError
from actors.internal.cell import Cell
from actors.internal.messages import Start, Failure, Terminate, Restart, Terminated


@pytest.fixture
def actor():
    actor = Mock(spec_set=Actor)
    actor.receive = Mock()
    actor.pre_start = Mock()
    actor.post_stop = Mock()
    return actor


@pytest.fixture
def supervisor():
    supervisor = Mock()
    supervisor.send_system_message = Mock()
    return supervisor


@pytest.fixture
def running_cell(actor, supervisor):
    cell = Cell(lambda: actor, Mock(), Mock(), supervisor)
    cell.handle_system_message(Start)
    return cell


def test_handle_message_invokes_receive_on_actor(actor, running_cell):
    message = object()
    running_cell.handle_message(Envelope(message, None))
    actor.receive.assert_called_once_with(message)


def test_handle_message_should_raise_if_actor_not_created(actor):
    cell = Cell(lambda: actor, Mock(), Mock(), Mock())
    with pytest.raises(Exception):
        cell.handle_message(Mock())


def test_start_constructs_instance():
    factory = Mock()
    cell = Cell(factory, Mock(), Mock(), Mock())
    cell.handle_system_message(Start)
    factory.assert_called_once_with()


def test_start_calls_start_hook(actor):
    cell = Cell(lambda: actor, Mock(), Mock(), Mock())
    cell.handle_system_message(Start)
    actor.pre_start.assert_called_once_with()


# Supervision

def _check_sent_failure_message(expected_sender, receiver, expected_exception):
    message = receiver.send_system_message.call_args[0][0]
    assert type(message) is Failure
    assert message.ref == expected_sender
    assert type(message.exception) is type(expected_exception)


def test_failure_in_message_handler_should_suspend_mailbox(actor, running_cell):
    actor.receive.side_effect = ValueError()
    running_cell.handle_message(Mock())
    assert running_cell._mailbox.is_suspended()


def test_failure_in_message_handler_sends_failure_message_to_supervisor(actor, supervisor, running_cell):
    actor.receive.side_effect = ArithmeticError()
    running_cell.handle_message(Mock())
    _check_sent_failure_message(ActorRef(running_cell), supervisor, ArithmeticError())


def test_failure_in_start_hook_should_send_failure_to_supervisor(actor, supervisor):
    actor.pre_start.side_effect = AttributeError()
    cell = Cell(lambda: actor, Mock(), Mock(), supervisor)
    cell.handle_system_message(Start)
    actor.pre_start.assert_called_once_with()
    _check_sent_failure_message(ActorRef(cell), supervisor, ActorInitializationError())


def test_sends_failure_if_factory_does_not_return_an_actor(supervisor):
    cell = Cell(lambda: object(), Mock(), Mock(), supervisor)
    cell.handle_system_message(Start)
    _check_sent_failure_message(ActorRef(cell), supervisor, ActorInitializationError())


def test_failure_in_restart_hook_should_send_failure_to_supervisor(actor, supervisor, running_cell):
    actor.pre_restart.side_effect = ArithmeticError()
    running_cell.handle_system_message(Restart)
    _check_sent_failure_message(ActorRef(running_cell), supervisor, ActorInitializationError())


def test_failure_in_stop_hook_should_not_send_failure_to_supervisor(actor, supervisor, running_cell):
    actor.post_stop.side_effect = AttributeError()
    running_cell.handle_system_message(Terminate)

    actor.post_stop.assert_called_once_with()
    for call in supervisor.send_system_message.call_args_list:
        assert not isinstance(call[0][0], Failure)


def test_failure_in_start_hook_stops_actor(actor, supervisor, running_cell):
    pass


def test_failure_in_restart_hook_stops_actor(actor, supervisor, running_cell):
    pass


def test_context_properties(actor, supervisor, running_cell):
    sender = object()

    global actual_sender, actual_supervisor, actual_self_ref
    actual_sender = actual_supervisor = actual_self_ref = None

    def store_context(message):
        global actual_sender, actual_supervisor, actual_self_ref
        actual_sender = actor.context.sender
        actual_supervisor = actor.context.supervisor
        actual_self_ref = actor.context.self_ref

    actor.receive.side_effect = store_context

    running_cell.handle_message(Envelope(Mock(), sender))
    assert actor.receive.call_count == 1

    assert actual_sender is sender
    assert actual_supervisor is supervisor
    assert actual_self_ref == ActorRef(running_cell)
