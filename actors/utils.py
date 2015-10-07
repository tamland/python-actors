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

from collections import namedtuple
from actors.actor import Actor
from .future import Promise
from .ref import ActorRef


class PromiseActorRef(ActorRef):
    def __init__(self):
        super(PromiseActorRef, self).__init__(None)
        self.promise = Promise()

    def tell(self, message, sender=None):
        self.promise.complete(message)


def ask(actor, message):
    """
    Send a message to `actor` and return a future that will hold the result.

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


class AsyncCountDownLatch(Actor):
    CountDown = object()
    Done = object()
    Start = namedtuple('Start', ['count'])

    def __init__(self):
        self._count = -1
        self._reply_to = None

    def receive(self, message):
        if message is AsyncCountDownLatch.CountDown:
            self._count -= 1
            if self._count == 0:
                self._reply_to.tell(AsyncCountDownLatch.Done)
        elif type(message) is AsyncCountDownLatch.Start:
            self._count = message.count
            self._reply_to = self.context.sender
