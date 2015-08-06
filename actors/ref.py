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

from . import no_sender, Envelope


class ActorRef(object):

    def __init__(self, actor_cell):
        self._actor_cell = actor_cell

    def tell(self, message, sender=no_sender):
        if sender is not no_sender and not isinstance(sender, ActorRef):
            raise ValueError("Sender must be actor reference")

        self._actor_cell.send_message(Envelope(message, sender))

