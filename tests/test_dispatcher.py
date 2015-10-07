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
from actors.internal.dispatcher import Dispatcher
from actors.internal.executor import Executor
from actors.internal.mailbox import InternalMailbox
from .mock_compat import Mock


@pytest.fixture
def executor():
    return Mock(spec_set=Executor)


@pytest.fixture
def dispatcher(executor):
    return Dispatcher(executor)


def test_dispatch_should_enqueue_message(dispatcher):
    mailbox = Mock(spec_set=InternalMailbox)
    mailbox.is_closed.return_value = False

    message = object()
    dispatcher.dispatch(message, mailbox)
    mailbox.enqueue.assert_called_once_with(message)


def test_dispatch_should_execute_mailbox(executor, dispatcher):
    mailbox = Mock(spec_set=InternalMailbox)
    mailbox.has_messages.return_value = True
    mailbox.is_closed.return_value = False
    mailbox.is_scheduled.return_value = False

    dispatcher.dispatch(Mock(), mailbox)
    executor.submit.assert_called_once_with(mailbox.process_messages)


def test_dispatch_should_not_execute_on_unsuccessful_schedule(executor, dispatcher):
    mailbox = Mock(spec_set=InternalMailbox)
    mailbox.has_messages.return_value = True
    mailbox.is_closed.return_value = False
    mailbox.is_scheduled.return_value = False
    mailbox.set_scheduled.return_value = False

    dispatcher.dispatch(Mock(), mailbox)
    assert mailbox.set_scheduled.called
    assert not executor.submit.called


def test_should_shutdown_executor_when_no_actor_attached(executor, dispatcher):
    dispatcher.await_shutdown()
    executor.shutdown.assert_called_once_with()


def test_dispatch_should_not_deliver_when_mailbox_is_closed(executor, dispatcher):
    mailbox = Mock(spec_set=InternalMailbox)
    mailbox.has_messages.return_value = True
    mailbox.is_closed.return_value = True

    dispatcher.dispatch(Mock(), mailbox)
    dispatcher.dispatch_system(Mock(), mailbox)

    assert not mailbox.enqueue.called
    assert not mailbox.set_scheduled.called
    assert not executor.submit.called
