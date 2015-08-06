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

from __future__ import absolute_import
from __future__ import unicode_literals

import time
from threading import Event
from unittest.mock import Mock

from actors.dispatch.event_based import EventBasedDispatcher, State


def test_mailbox_scheduling():
    barrier = Event()
    dispatcher = EventBasedDispatcher()

    actor = Mock()
    actor.process_message = Mock()
    actor.process_message.side_effect = lambda *args, **kwargs: barrier.wait()
    actor.mailbox = dispatcher.create_mailbox()
    mailbox = actor.mailbox

    assert len(mailbox) == 0, "Prerequisite"
    assert mailbox.state == State.WAITING, "Prerequisite"

    dispatcher.dispatch(1, actor)
    time.sleep(1)

    # Dispatcher should have started processing
    assert len(mailbox) == 0
    assert actor.process_message.called
    assert mailbox.state == State.WORKING

    barrier.set()
    time.sleep(1)

    # Dispatcher should stop processing
    assert mailbox.state == State.WAITING
