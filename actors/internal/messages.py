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

from collections import namedtuple

Start = object()
Restart = object()
Resume = object()
Terminate = object()

Restart = "restart"
Terminate = "terminate"

Failure = namedtuple('Failure', ['ref', 'exception', 'traceback'])
Supervise = namedtuple('Supervise', ['ref'])
Terminated = namedtuple('Terminated', ['ref'])

DeadLetter = namedtuple('DeadLetter', ['message', 'sender', 'recipient'])
