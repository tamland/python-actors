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
from actors.actor import Actor


def as_proxy(actor_ref):
    """
    Create a proxy wrapper from an existing reference. The actor MUST implement the
    :class:`ProxyActor` interface.

    :param actor_ref: The actor reference.
    :type actor_ref: :class:`ActorRef`
    """
    return ProxyRef(actor_ref)


Invoke = namedtuple('Invoke', ['name', 'args', 'kwargs'])


class ProxyRef(object):

    def __init__(self, underlying):
        self._underlying = underlying

    def __getattr__(self, name):
        return lambda *args, **kwargs: \
            self._underlying.tell(Invoke(name, args, kwargs))


class ProxyActor(Actor):
    def receive(self, message):
        getattr(self, message.name)(*message.args, **message.kwargs)
