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

import six
from six.moves.queue import Queue, Empty
from collections import namedtuple


Failure = namedtuple('Failure', ['exc_info'])


class Timeout(Exception):
    pass


class Future(object):
    def __init__(self):
        self._result = Queue(maxsize=1)
        self._success_callback = None
        self._failure_callback = None

    def get(self, timeout=None):
        """
        Return value on success, or raise exception on failure.
        """
        result = None
        try:
            result = self._result.get(True, timeout=timeout)
        except Empty:
            raise Timeout()

        if isinstance(result, Failure):
            six.reraise(*result.exc_info)
        else:
            return result

    def on_success(self, callback):
        self._success_callback = callback

    def on_failure(self, callback):
        self._failure_callback = callback


class Promise(object):
    def __init__(self):
        self._future = Future()

    def complete(self, result):
        if isinstance(result, Failure):
            self.failure(result)
        else:
            self.success(result)

    def success(self, result):
        self._future._result.put(result)
        if self._future._success_callback:
            self._future._success_callback(self._future)

    def failure(self, result):
        self._future._result.put(Failure(result))
        if self._future._failure_callback:
            self._future._failure_callback(self._future)

    @property
    def future(self):
        return self._future
