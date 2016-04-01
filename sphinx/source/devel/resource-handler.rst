.. _cloudhandler:

Resource Management
===================

Resource management in OCCO is performed by Cloud Handler plugins. Although
their name is *Cloud* Handler, the interface and the model is generic enough to
support non-cloud-based resources too (e.g. Docker containers, common
processes, etc.)

OCCO is oblivious to the content of these resources. They can contain
pre-installed and pre-configured services, they can be raw resources set up
later by a :ref:`Service Composer <servicecomposer>`, or anything in-between.

Abstract Cloud Handler and generic functions
--------------------------------------------

.. automodule:: occo.resourcehandler
    :members:

Specialized backend implementations
-----------------------------------

.. automodule:: occo.plugins.resourcehandler

EC2 plugin
~~~~~~~~~~

.. automodule:: occo.plugins.resourcehandler.ec2
    :members:

NOVA plugin
~~~~~~~~~~~

.. automodule:: occo.plugins.resourcehandler.nova
    :members:

OCCI plugin
~~~~~~~~~~~

.. automodule:: occo.plugins.resourcehandler.occi
    :members:

CloudBroker plugin
~~~~~~~~~~~~~~~~~~

.. automodule:: occo.plugins.resourcehandler.cloudbroker
    :members:

Docker plugin
~~~~~~~~~~~~~

.. automodule:: occo.plugins.resourcehandler.docker
    :members:

