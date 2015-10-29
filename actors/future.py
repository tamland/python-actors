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
