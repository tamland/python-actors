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

import sys
import traceback
import pytest
from actors.utils import Promise
from .mock_compat import Mock


def test_get_should_return_on_success():
    promise = Promise()
    promise.success(1)
    assert promise.future.get() == 1


def test_get_should_raise_on_failure():
    promise = Promise()
    try:
        1/0
    except ZeroDivisionError:
        traceback.print_exc()
        promise.failure(sys.exc_info())

    with pytest.raises(ZeroDivisionError):
        promise.future.get()


def test_calls_callback_on_success():
    callback = Mock()
    promise = Promise()
    promise.future.on_success(callback)
    promise.success(None)
    callback.assert_called_once_with(promise.future)


def test_calls_callback_on_failure():
    callback = Mock()
    promise = Promise()
    promise.future.on_failure(callback)
    promise.failure(None)
    callback.assert_called_once_with(promise.future)
