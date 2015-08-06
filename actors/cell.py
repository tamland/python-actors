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

import logging
from actors.ref import ActorRef


logger = logging.getLogger(__name__)


class ActorCell(object):

    def __init__(self, actor, system, dispatcher):
        self._impl = actor
        self._system = system
        self._dispatcher = dispatcher
        self._stopped = False
        self.ref = ActorRef(self)
        self._impl.ref = self.ref
        self.mailbox = dispatcher.create_mailbox()

    def send_message(self, envelope):
        if not self._stopped:
            self._dispatcher.dispatch(envelope, self)
        else:
            raise NotImplementedError()

    def process_message(self, envelope):
        self._impl.sender = envelope.sender
        try:
            self._impl.receive(envelope.message)
        except BaseException as e:
            logger.exception("Error in actor: %r" % e)
        self._impl.sender = None

    def _flush_mailbox(self):
        raise NotImplementedError()

    def stop(self):
        self._dispatcher.detach(self)
        self._dispatcher.shutdown()
