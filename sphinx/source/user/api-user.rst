.. _api-user:

Usage
=====

Command line tools
------------------

OCCOpus can be used via CLI commands to create, manage and tear down infrastructures. The commands and their usages are described below.

occo-infra-start
~~~~~~~~~~~~~~~~

This script builds up an infrastructure. It requires a ``configuration file``
as a parameter, and builds the corresponding infrastructure using an Enactor +
InfraProcessor pair. Returns the infra_id, and also stores it in the Information
Broker.

On error during creating the infrastructure it rolls back everything to the
initial state. The user can also stop the process manually by executing a SIGINT
(Ctrl + C). The resources will be rolled back in this case as well.

The script provides no lifecycle-management, as it detaches from the
infrastructure after building it.

occo-infra-stop
~~~~~~~~~~~~~~~

This script tears down an infrastructure using OCCO-CloudHandler and
OCCO-InfraProcessor.

An infra_id is required.

**Usage:** 

``occo-infra-stop [-h] [--cfg CFG_PATH] -i INFRA_ID``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``-i INFRA_ID:`` provides the identifier of the infrastructure to destroy

occo-manager-service
~~~~~~~~~~~~~~~~~~~~

This script launches occo as a web service. The occo manager service can create,
maintain and manipulate the infrastructures started through the service. This
service provides a restful interface described by `REST API`_.

**Usage:** 

``occo-manager-service [-h] [--cfg CFG_PATH] [--host HOST] [--port PORT]
[--parallelize]``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--host HOST:`` (optional) sets the host for the web service to be assigned to [default: 127.0.0.1]
    * ``--port PORT:`` (optional) sets the port for the web service to be assigned to [default: 5000]
    * ``--parallelize:`` (optional) parallelize processing instructions (default: sequential)

REST API
--------

.. autoflask:: occo.api.rest:app
   :endpoints: 
   :include-empty-docstring:

Python API
----------

Basic features for OCCO-based applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.api.occoapp
    :members:

Infrastructure Manager
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: occo.api.manager
    :members:

