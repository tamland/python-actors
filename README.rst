============
PythonActors
============

.. image:: https://img.shields.io/pypi/v/actors.svg
    :target: https://pypi.python.org/pypi/actors

.. image:: https://img.shields.io/travis/tamland/python-actors.svg

.. image:: https://img.shields.io/coveralls/tamland/python-actors.svg



``actors`` is a small actor framework for in-process asynchronous message passing in Python.


Features
--------

* Low overhead. Can run any number of actors on a single thread.
* Built-in supervision hierarchy and fault tolerance.
* Extensible with dispatchers and executors.


Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/actors/>`_ using ``pip``:

.. code-block:: bash

    $ pip install actors


Quick start
-----------

Hello world!
~~~~~~~~~~~~

.. code-block:: python

    from actors import Actor, ActorSystem

    class Greeter(Actor):
        def receive(self, message):
            print("Hello %s" % message)

    with ActorSystem() as system:
        greeter = system.actor_of(Greeter)
        greeter.tell("world")



Creating the actor system
~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ActorSystem`` is responsible for creating, configuring and managing a group of actors,
dispatchers and other parts of the actor framework. Normally one system should be created per
application. When ``system.terminate()`` is called (or the context manager exit) all actors are
stopped immediately.


Creating actors
~~~~~~~~~~~~~~~

To create an actor, extend the ``Actor`` base class and implement ``receive``, then use
the ``actor_of`` factory method spawn an actor instance.

To pass constructor arguments to the actor, use ``functools.partial``.

Example:

.. code-block:: python

    from functools import partial

    class Greeter(Actor):
        def __init__(self, format):
            self._format = format
        ...

    greeter = system.actor_of(partial(Greeter, "Hello %s!")


The ``Actor`` base class additionally provides hooks for specializing lifetime and supervisor
behaviour. See API documentation for details.


Sending messages
~~~~~~~~~~~~~~~~

Messages can be sent by invoking ``tell`` on an ``ActorRef`` which will send one-way message (also
known as “fire-and-forget”), or with ``ask`` which returns a ``Future``` with a possible reply.
In both cases, messages are sent asynchronously.

Examples:

.. code-block:: python

    from actors.utils.ask import ask

    # send a one-way message
    greeter.tell("Hello!")

    # get a future with a reply
    reply = ask(greeter, "Hello?")

    # block until the reply is ready
    answer = reply.get()


Replying
~~~~~~~~

When sending messages using ``tell`` the sender can be supplied along with
the message as the second argument.

To "reply" to a message, simply send a message to its sender.

Example:

.. code-block:: python

    class Greeter(Actor):
        def receive(self, message):
            if message.startswith("Hello"):
                # reply to the sender
                self.sender.tell('Hi there!')


Supervision and fault tolerance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO


Documentation
-------------

Documentation is available at http://pythonhosted.org/actors/.
