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

import threading
import pytest
from actors.internal.executor import Executor


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




