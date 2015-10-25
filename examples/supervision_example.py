# -*- coding: utf-8 -*-
import logging
import time
import random
from actors import Actor, ActorSystem, Directive

logging.basicConfig(level=logging.DEBUG)


class Crash(Exception):
    pass


StartGreeting = object()


class Greeter(Actor):
    def post_restart(self):
        print("Greeter restarted")

    def receive(self, message):
        if random.randint(0, 3) == 0:
            raise Crash()
        print("Hello %s" % message)


class Supervisor(Actor):
    @staticmethod
    def supervisor_strategy(exception):
        try:
            raise exception
        except Crash:
            return Directive.Restart
        except:
            return Directive.Stop

    def __init__(self):
        self._greeter = None

    def receive(self, message):
        if message is StartGreeting:
            self._greeter = self.context.actor_of(Greeter)
        else:
            # Forward the message to greeter
            self._greeter.tell(message, self.context.sender)


system = ActorSystem()
supervisor = system.actor_of(Supervisor)
supervisor.tell(StartGreeting)

try:
    while True:
        supervisor.tell("world")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass

system.terminate()
