.. _api-user:

Usage
=====

Command line tools
------------------

Occopus can be used via CLI commands to build, maintain, scale and destroy infrastructures. The commands and their usages are described below.

occopus-build
~~~~~~~~~~~~~

This command deploys an infrastructure based on an infrastructure description.

On error during creating the infrastructure it rolls back everything to the
initial state. The user can also stop the process manually by executing a SIGINT
(Ctrl + C). Allocation of resources will be rolled back in this case as well.

Once the infrastructure is successfully built, Occopus exits. This command provides no lifecycle-management.

**Usage:** 

.. code:: yaml

 occopus-build [-h] 
               [--cfg CFG_PATH] 
               [--auth_data_path AUTH_DATA_PASS] 
               [--parallelize]
               infra_def

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--parallelize:`` (optional) parallelize processing instructions e.g. independent nodes are created parallel (default: sequential)
    * ``infra_def:`` file containing an infrastructure definition

**Return type:**
    On successful finish it returns the identifier of the infrastructure. The identifier can be stored or listed by the occopus-maintain command. 

occopus-destroy
~~~~~~~~~~~~~~~

This command destroys an infrastructure including all of its nodes built previously by Occopus. No recover is possible.

**Usage:** 

.. code:: yaml

 occopus-destroy [-h] 
                 [--cfg CFG_PATH] 
                 [--auth_data_path AUTH_DATA_PATH] 
                 -i INFRA_ID

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``-i INFRA_ID:`` identifier of the infrastructure to destroy

occopus-maintain
~~~~~~~~~~~~~~~~

This command is capable of maintaining an infrastructure built by Occopus. Maintenance includes health checking, recovery and scaling. It can also list available infrastructure or can provide details on an infrastructure.

**Usage:** 

.. code:: yaml

 occopus-maintain [-h] 
                  [--cfg CFG_PATH] 
                  [--auth_data_path AUTH_DATA_PATH] 
                  [-l|--list] 
                  [-r|--report]
                  [-i INFRA_ID] 
                  [-c|--cyclic] 
                  [-t INTERVAL] 

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``-l, --list:`` (optional) list the built pieces of infrastructure
    * ``-r, --report:`` (optional) reports about an infrastructure
    * ``-i INFRA_ID:`` (optional) identifier of the infrastructure to maintain
    * ``-c, --cyclic:`` (optional) performs continuous maintenance
    * ``-t INTERVAL:`` (optional) specifies the time in seconds between maintenance sessions (default: 10)

occopus-scale
~~~~~~~~~~~~~

This command registers scaling requests for a given node in an infrastructure. With scaling the instance count of a node can be increased or decreased by a given number. Scaling requests are handled and realized by the occopus-maintain command.

**Usage:** 

.. code:: yaml

 occopus-scale [-h] 
               [--cfg CFG_PATH]
               [--auth_data_path AUTH_DATA_PATH] 
               -i INFRA_ID 
               -n|--node NODE 
               -c|--count COUNT

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``-i INFRA_ID:`` identifier of the infrastructure which contains the node to scale
    * ``-n NODE, --node NODE:`` name of the node to scale
    * ``-c COUNT, --count COUNT:`` positive/negative number expressing the direction and magnitude of scaling (positive: scale up; negative: scale down)

occopus-import
~~~~~~~~~~~~~~

This command imports i.e. loads the node definitions from file to the database behind Occopus. 

.. important::

  Each time a node definition file changes, this command must be executed since Occopus takes node definitions from its database!

**Usage:**

.. code:: yaml

 occopus-import [-h] 
                [--redisconf REDISCONF] 
                datafile

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--redisconf REDISCONF:`` (optional) loads database access configuration from REDISCONF file (default:None) if undefined, file named *redis_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``datafile:`` file containing node definition(s)

occopus-rest-service
~~~~~~~~~~~~~~~~~~~~

This command launches occopus as a web service. The occopus rest service can create, maintain, scale and destroy any infrastructure built by the service. This service provides a restful interface described by `REST API`_.

**Usage:** 

.. code:: yaml

 occopus-rest-service [-h] 
                      [--cfg CFG_PATH] 
                      [--auth_data_path AUTH_DATA_PATH] 
                      [--host HOST]
                      [--port PORT]
                      [--parallelize]

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--host HOST:`` (optional) sets the host for the service to be assigned to (default: 127.0.0.1)
    * ``--port PORT:`` (optional) sets the port for the service to be assigned to (default: 5000)
    * ``--parallelize:`` (optional) parallelize processing instructions (default: sequential)

REST API
--------

.. autoflask:: occo.api.rest:app
   :endpoints: 
   :include-empty-docstring:

Python API
----------

Occopus provides a Python API which can be used to implement Occopus-based applications in a unified way. The API gives the possibility to utilise Occopus functionalities inside an application. To read about this possibility, please go to the API section of the Developers' guide.

