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

from actors.future import Promise
from actors.ref import ActorRef


class PromiseActorRef(ActorRef):
    def __init__(self):
        super(PromiseActorRef, self).__init__(None)
        self.promise = Promise()

    def tell(self, message, sender=None):
        self.promise.complete(message)


def ask(actor, message):
    """
    Send a message to `actor` and return a :class:`Future` holding a possible
    reply.

    To receive a result, the actor MUST send a reply to `sender`.

    :param actor:
    :type actor: :class:`ActorRef`.

    :param message:
    :type message: :type: Any

    :return: A future holding the result.
    """
    sender = PromiseActorRef()
    actor.tell(message, sender)
    return sender.promise.future

