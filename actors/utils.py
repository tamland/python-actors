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

from __future__ import absolute_import
from __future__ import unicode_literals

from .future import Promise

__all__ = [
    'Future',
    'Promise',
    'ask',
]


class PromiseActorRef(object):
    def __init__(self):
        self.promise = Promise()

    def tell(self, message):
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


def await(future):
    raise NotImplemented()