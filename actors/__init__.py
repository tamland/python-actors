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


__all__ = [
    'no_sender',
    'Actor',
    'ActorContext',
    'ActorSystem',
    'ActorRef',
    'Directive',
]

from actors.internal import messages

Envelope = namedtuple('Envelope', ['message', 'sender'])

no_sender = None


class ActorInitializationError(Exception):
    pass


class Directive(object):
    Stop = messages.Terminate
    Restart = messages.Restart
    Resume = messages.Resume


def default_supervisor_strategy(exception):
    if isinstance(exception, ActorInitializationError):
        return Directive.Stop
    return Directive.Restart


from .actor import Actor
from .context import ActorContext
from .system import ActorSystem
from .ref import ActorRef
