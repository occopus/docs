.. _api-user:

Usage
=====

Command line tools
------------------

Occopus can be used via CLI commands to create, manage and tear down infrastructures. The commands and their usages are described below.

occopus-build
~~~~~~~~~~~~~

This script deploys an infrastructure based on an infrastructure description
and configuration.

On error during creating the infrastructure it rolls back everything to the
initial state. The user can also stop the process manually by executing a SIGINT
(Ctrl + C). Allocation of resources will be rolled back in this case as well.

Once the infrastructure is successfully deployed, Occopus exits. This script provides no lifecycle-management.

**Usage:** 

``occopus-build [-h] [--cfg CFG_PATH] [--auth_data_path AUTH_DATA_PASS] [--parallelize] [--listips] infra_def``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authorisation file
    * ``--parallelize:`` (optional) parallelize processing instructions (default: sequential)
    * ``--listips:`` (optional) on exit it logs the list of node and ip addresses 
    * ``infra_def:`` file containing an infrastructure definition

**Return type:**
    On sucessful finish it returns the identifier of the infrastructure. Note:
    you must store the identifier for further instruction on the infrastructure.

occopus-destroy
~~~~~~~~~~~~~~~

This script destroys an infrastructure built previously by Occopus. All the nodes
are destoyed, no recover is possible.

**Usage:** 

``occopus-destroy [-h] [--cfg CFG_PATH] [--auth_data_path AUTH_DATA_PATH] -i INFRA_ID``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authorisation file
    * ``-i INFRA_ID:`` provides the identifier of the infrastructure to destroy

occopus-manage
~~~~~~~~~~~~~~

This script is capable of attaching to infrastructures deployed by Occopus, and
manage them. It can also list the active infrastructures in Occopus.

**Usage:** 

``occopus-destroy [-h] [--cfg CFG_PATH] [--auth_data_path AUTH_DATA_PATH] [-i INFRA_ID] [-l|--list] [-t INTERVAL] [-c|--cyclic] [-r|--report]``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authorisation file
    * ``-i INFRA_ID:`` (optional) provides the identifier of the infrastructure to destroy
    * ``-l, --list:`` (optional) list the active infrastructures in the Occopus database
    * ``-t INTERVAL:`` (optional) specifies the time between management sessions (default: 10)
    * ``-c, --cyclic:`` (optional) performs continuous management
    * ``-r, --report:`` (optional) reports about the infrastructure

occopus-scale
~~~~~~~~~~~~~

This script scales a given node of an infrastructure up or down by a given number.

**Usage:** 

``occopus-scale [-h] [--cfg CFG_PATH] [--auth_data_path AUTH_DATA_PATH] -i INFRA_ID -n|--node NODE -c|--count COUNT``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authorisation file
    * ``-i INFRA_ID:`` provides the identifier of the infrastructure which contains the node to scale
    * ``-n NODE, --node NODE:`` provides the name of the node to scale
    * ``-c COUNT, --count COUNT:`` positive/negative number expressing the direction and magnitude of scaling (positive: scale up; negative: scale down)

occopus-import
~~~~~~~~~~~~~~

This script imports i.e. loads the node definitions from file to the database
behind Occopus. 

**IMPORTANT**: each time a node definition changes, this script must be used!

**Usage:**

``occopus-import [-h] [--redisconf REDISCONF] datafile``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--redisconf REDISCONF:`` (optional) loads database access configuration from REDISCONF file
    * ``datafile:`` file containing node definitions

occopus-rest-service
~~~~~~~~~~~~~~~~~~~~

This script launches occopus as a web service. The occopus rest service can create,
maintain and manipulate the infrastructures started through the service. This
service provides a restful interface described by `REST API`_.

**Usage:** 

``occopus-rest-service [-h] [--cfg CFG_PATH] [--auth_data_path AUTH_DATA_PATH] [--host HOST] [--port PORT]
[--parallelize]``

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) loads configuration from CFG_PATH file
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authorisation file
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

Occopus provides a Python API which can be used to implement Occopus-based applications in a unified way. The API gives the possibility to utilise Occopus functionalities inside an application. To read about this possibility, please go to the API section of the Developers' guide.

