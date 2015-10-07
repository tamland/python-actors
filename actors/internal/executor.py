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

import logging
from threading import Thread
from six.moves.queue import Queue


logger = logging.getLogger(__name__)


class Executor(object):
    _INTERRUPT = object()

    def __init__(self, num_workers=1):
        super(Executor, self).__init__()
        self._queue = Queue()
        self._workers = []

        for _ in range(num_workers):
            th = Thread(target=self._work)
            th.start()
            self._workers.append(th)

    def submit(self, task):
        self._queue.put(task)

    def shutdown(self):
        for _ in self._workers:
            self._queue.put(self._INTERRUPT)
        for worker in self._workers:
            worker.join()

    def _work(self):
        while True:
            task = self._queue.get(block=True)
            if task is self._INTERRUPT:
                break
            try:
                task()
            except BaseException as e:
                logger.exception(e)
