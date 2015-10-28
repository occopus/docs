.. _api-user:

Usage
=====

Command line tools
------------------

OCCO can be used via CLI commands to create, manage and tear down infrastructures. The commands and their usages are described below.

occo-infra-start
~~~~~~~~~~~~~~~~

This script deploys an infrastructure based on an infrastructure description
and configuration.

On error during creating the infrastructure it rolls back everything to the
initial state. The user can also stop the process manually by executing a SIGINT
(Ctrl + C). Allocation of resources will be rolled back in this case as well.

Once the infrastructure is successfully deployed, OCCO exits. This script provides no lifecycle-management.

**Usage:** 

``occo-infra-start [-h] [--cfg CFG_PATH] [--parallelize] [--listips] infra_def``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--parallelize:`` (optional) parallelize processing instructions (default: sequential)
    * ``--listips:`` (optional) on exit it logs the list of node and ip addresses 
    * ``infra_def:`` file containing an infrastructure definition

**Return type:**
    On sucessful finish it returns the identifier of the infrastructure. Note:
    you must store the identifier for further instruction on the infrastructure.

occo-infra-stop
~~~~~~~~~~~~~~~

This script destroys an infrastructure built previously by OCCO. All the nodes
are destoyed, no recover is possible.

**Usage:** 

``occo-infra-stop [-h] [--cfg CFG_PATH] -i INFRA_ID``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``-i INFRA_ID:`` provides the identifier of the infrastructure to destroy

occo-import-node
~~~~~~~~~~~~~~~~

This script imports i.e. loads the node definitions from file to the database
behind OCCO is using. 

**IMPORTANT**: each time a node definition changes, this script must be used!

**Usage:**

``occo-import-node [-h] redis_data``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``redis_data`` file describing the database access and the location of the
      node definitions, see the following example for this file.

.. code:: yaml

    redis_data.yaml:
        kvs: !KeyValueStore
            protocol: redis
            host: localhost
            port: 6379
            db: 0
            altdbs:
                node_def: 1
        init_data: !yaml_import
            url: file://uds_init_data.yaml

The example above assumes that the name of the file containing node definitions is "uds_init_data.yaml".

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

OCCO provides a Python API which can be used to implement OCCO-based applications in a unified way. The API gives the possibility to utilise OCCO functionalities inside an application. To read about this possibility, please go to the :ref:`API section of Developers' guide<api>`.

