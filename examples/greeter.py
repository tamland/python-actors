from actors import Actor, ActorSystem


class Greeter(Actor):
    def receive(self, message):
        print("Hello %s" % message)


with ActorSystem() as system:
    greeter = system.actor_of(Greeter)
    greeter.tell("world")
