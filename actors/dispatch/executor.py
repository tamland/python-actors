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

from threading import Thread
from six.moves.queue import Queue


class Executor(object):
    _TERMINATE = object()

    def __init__(self):
        super(Executor, self).__init__()
        self._queue = Queue()
        self._workers = []
        self._stopped = False

        num_workers = 1
        for _ in range(num_workers):
            th = Thread(target=self._work)
            th.daemon = True
            th.start()
            self._workers.append(th)

    def submit(self, task):
        self._queue.put(task)

    def shutdown(self):
        for _ in self._workers:
            self._queue.put(self._TERMINATE)
        for worker in self._workers:
            worker.join()

    def _work(self):
        while True:
            task = self._queue.get(block=True)
            if task is self._TERMINATE:
                break
            try:
                task()
            except BaseException:
                pass
