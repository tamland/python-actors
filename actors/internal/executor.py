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

    def join(self):
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
