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
