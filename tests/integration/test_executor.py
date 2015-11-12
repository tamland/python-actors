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

import threading
from actors.internal.executor import Executor
from ..mock_compat import Mock


def test_executor_spawns_n_thread():
    threads_before = threading.active_count()
    executor = Executor(20)
    assert threading.active_count() == threads_before + 20
    executor.shutdown()


def test_shutdown_terminates_threads():
    threads_before = threading.active_count()
    executor = Executor(20)

    for i in range(10):
        executor.submit(lambda: None)

    executor.shutdown()
    assert threading.active_count() == threads_before


def test_executor_ignores_errors_in_task():
    executor = Executor()

    task1 = Mock()
    task1.side_effect = KeyError
    task2 = Mock()

    executor.submit(task1)
    executor.submit(task2)
    executor.shutdown()

    task1.assert_called_once_with()
    task2.assert_called_once_with()
