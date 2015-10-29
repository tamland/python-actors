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
