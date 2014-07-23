Component Communication in OCCO
===============================

Communication in OCCO is performed through abstract interfaces. Currently,
these interfaces are implemented using the AMQP protocol using ``pika``.

Three abstract interfaces are provided:
 - Asynchronous message passing

   Messages are sent asynchronously, using a given rouing key. Only
   ACKnowledgement is expected.
 - RPC calls

   The message processor is expected to return a result. Currently, there is no
   support for timeout or interruption.
 - Event-driven message processing

   A processor function must be provided by the client code. Whenever a message
   arrives, the processor function is called. If the message was an RPC
   message, the result is returned to the caller.

The abstract classes implement the *abstract factory* pattern. That is,
implementing classes should not be instantiated directly. Instantiating an
abstract class will check the ``protocol`` specified in the configuration,
and instantiates the real backend automatically.

.. warning::
    AMQP implementations require context management.

Example
-------
``config.yaml``

.. code-block:: yaml

    mqconfig:
        protocol: amqp
        host: 192.168.152.184
        vhost: test
        exhange: ''
        routing_key: test
        queue: test
        user: test
        password: test

``async_producer_example.py``

.. code-block:: python

    import occo.util.config as config
    import occo.util.communication as comm

    with open('config.yaml') as f
        cfg = config.DefaultYAMLConfig(f)

    prod = comm.AsynchronProducer(**cfg.mqconfig)
    with prod:
        prod.push_message('test message')

``rpc_producer_example.py``

.. code-block:: python

    import occo.util.config as config
    import occo.util.communication as comm

    with open('config.yaml') as f
        cfg = config.DefaultYAMLConfig(f)

    prod = comm.RPCProducer(**cfg.mqconfig)
    with prod:
        try:
            data = prod.push_message('test message')
        except CommunicationError as e:
            print e
        except ApplicationError as e:
            # do application specific error handling here
        else:
            print data

``infinite_consumer_example.py``

.. code-block:: python

    import occo.util.config as config
    import occo.util.communication as comm

    with open('config.yaml') as f
        cfg = config.DefaultYAMLConfig(f)

    def core_func(msg):
        print msg

    cons = comm.EventDrivenConsumer(core_func, **cfg.mqconfig)
    with cons:
        cons.start_consuming()

``interruptable_consumer_example.py``

.. code-block:: python

    import occo.util.config as config
    import occo.util.communication as comm
    import threading

    with open('config.yaml') as f
        cfg = config.DefaultYAMLConfig(f)

    def core_func(msg):
        print msg

    cancel = threading.Event()
    cons = comm.EventDrivenConsumer(core_func,
                                    cancel_event=cancel,
                                    **cfg.mqconfig)
    t = threading.Thread(cons)
    with cons:
        t.start()
        threading.sleep(10)
        cancel.set()
        t.join()

Abstract Communication Interfaces
---------------------------------
.. automodule:: occo.util.communication.comm
    :members:
    :special-members:

AMQP Implementation of Abstract Interfaces
------------------------------------------
.. automodule:: occo.util.communication.mq
    :members:
    :special-members:
