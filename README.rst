============
PythonActors
============

A python actor framework.

.. image:: https://img.shields.io/pypi/v/actors.svg
    :target: https://pypi.python.org/pypi/actors


Features
--------

* Easy to build concurrency with the actor model.
* Lightweight. Can run millions of actors on a single thread.
* Integrated supervision for managing actor lifetime and faults.
* Extensible with new executors and dispatchers.
* An Akka-like API.


Installation
------------

Install from `PyPI <https://pypi.python.org/pypi/actors/>`_ using ``pip``:

.. code-block:: bash

    $ pip install actors


Obligatory greeter
------------------

.. code-block:: python

    from actors import Actor, ActorSystem

    class Greeter(Actor):
        def receive(self, message):
            print("Hello %s" % message)

    system = ActorSystem()
    greeter = system.actor_of(GreetingActor)
    greeter.tell("world")
    system.terminate()


Documentation
-------------

Documentation is available at http://pythonhosted.org/actors/.
