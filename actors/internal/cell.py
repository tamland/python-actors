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

import logging
import traceback

import actors.actor
import actors.context
import actors.system
from actors import ActorInitializationError, Envelope
from actors.actor import Actor
from actors.ref import ActorRef, InternalRef
from actors.internal.messages import Start, Terminate, Failure, Supervise, Terminated, Restart, \
    DeadLetter
from actors.internal.mailbox import InternalMailbox

logger = logging.getLogger(__name__)


class Cell(object):

    def __init__(self, actor_factory, system, dispatcher, parent):
        self._actor_factory = actor_factory  # Creates actor instances
        self._actor = None
        self._system = system
        self._dispatcher = dispatcher
        self._mailbox = InternalMailbox(dispatcher, self, dispatcher.throughput)
        self._dispatcher.attach(self._mailbox)

        self._parent = parent
        self._children = []
        self._self_ref = InternalRef(self)

        self._context = actors.context.ActorContext(system, self._self_ref)
        self._context.self_ref = ActorRef(self)

    def send_message(self, message, sender):
        if not self._mailbox.is_closed():
            self._dispatcher.dispatch(Envelope(message, sender), self._mailbox)
        else:
            self._system.dead_letters.tell(DeadLetter(message, sender, self._self_ref))

    def send_system_message(self, message):
        if not self._mailbox.is_closed():
            self._dispatcher.dispatch_system(message, self._mailbox)

    def handle_message(self, envelope):
        assert self._actor is not None
        try:
            self._context.sender = envelope.sender
            self._context.supervisor = self._parent
            self._actor.context = self._context
            self._actor.receive(envelope.message)
        except BaseException as e:
            self._on_failure(e)
        self._actor.context = None

    def handle_system_message(self, message):
        if message is Start:
            try:
                assert self._actor is None
                self._actor = self._actor_factory()
                assert isinstance(self._actor, Actor)
                self._actor.pre_start()
                # logger.debug("created actor %r" % self)
            except BaseException as e:
                self._on_failure(ActorInitializationError())

        # Directives from supervisor
        elif message is Restart:
            try:
                self._actor.pre_restart()
                self._actor = self._actor_factory()
                assert isinstance(self._actor, Actor)
                self._actor.post_restart()
                self._mailbox.resume()
                logger.debug("Actor %s restarted" % self)
            except BaseException as e:
                # TODO: use a different exception
                self._on_failure(ActorInitializationError())

        elif message is Terminate:
            self._mailbox.close()
            for child in self._children:
                child.send_system_message(Terminate)
            self._dispatcher.detach(self._mailbox)
            try:
                self._actor.post_stop()
            except BaseException:
                logger.warn("Failure in post_stop", exc_info=True)
            self._actor = None

            for envelope in self._mailbox.flush_messages():
                self._system.dead_letters.tell(DeadLetter(
                    envelope.message, envelope.sender, self._self_ref))

        elif type(message) is Supervise:
            try:
                assert isinstance(message.ref, InternalRef)
                self._children.append(message.ref)
            except (AttributeError, AssertionError) as e:
                logger.error("Failed to remove child", exc_info=True)

        elif type(message) is Terminated:
            try:
                assert isinstance(message.ref, InternalRef)
                assert message.ref in self._children
                self._children.remove(message.ref)
            except (KeyError, AttributeError, AssertionError):
                logger.error("Failed to remove child", exc_info=True)

        elif type(message) is Failure:
            try:
                directive = self._actor.__class__.supervisor_strategy(message.exception)
                assert directive is not None
            except BaseException:
                logger.error("Failed to get directive.")
            else:
                logger.info("Failure in child %r, exception: %s, directive: %r",
                            message.ref, type(message.exception).__name__, directive)
                message.ref.send_system_message(directive)
        else:
            logger.error("Got unknown system message '%r'", message)

    def _on_failure(self, exception):
        self._mailbox.suspend()
        if self._parent:
            msg = Failure(self._self_ref, exception, traceback.format_exc())
            self._parent.send_system_message(msg)
