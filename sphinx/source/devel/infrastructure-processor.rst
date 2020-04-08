.. _infraprocessor:
.. _IP:

Infrastructure Processor
========================

.. index::
    pair: Infrastructure Processor; InfraProcessor

Generic Infrastructure Processor component
------------------------------------------

Abstract InfraProcessor interface
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.infraprocessor
    :members:
    :undoc-members:

Default InfraProcessor implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.plugins.infraprocessor.basic_infraprocessor
    :members:
    :undoc-members:


Preparing node definitions for instantiation
--------------------------------------------

.. automodule:: occo.infraprocessor.node_resolution
    :members:
    :undoc-members:

Supporting Chef and cloud-init
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.plugins.infraprocessor.node_resolution.cloudinit
    :members:
    :undoc-members:

Supporting Docker
~~~~~~~~~~~~~~~~~

.. automodule:: occo.plugins.infraprocessor.node_resolution.docker
    :members:
    :undoc-members:

Waiting for nodes to be created
-------------------------------

Abstract interface and default behaviour
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.infraprocessor.synchronization
    :members:
    :undoc-members:

Generic primitives to be used with synchronization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.infraprocessor.synchronization.primitives
    :members:
    :undoc-members:
