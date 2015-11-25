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


@pytest.mark.xfail
def test_should_shutdown_executor_when_no_actors_attached(executor, dispatcher):
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
