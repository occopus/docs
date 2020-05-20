.. _user-doc-api-user:

Usage
#####

.. _api-user_cli:

Command line tools
******************

Occopus can be used via CLI commands to build, maintain, scale and destroy infrastructures. The commands and their usages are described below.

.. _api-user_buildcommand:

occopus-build
=============

This command deploys an infrastructure based on an infrastructure description.

On error during creating the infrastructure it rolls back everything to the
initial state. The user can also stop the process manually by executing a SIGINT
(Ctrl + C). Allocation of resources will be rolled back in this case as well.

Once the infrastructure is successfully built, Occopus exits. This command provides no lifecycle-management.

**Usage:**

.. code:: bash

 occopus-build [-h]
               [--cfg CFG_PATH]
               [--auth_data_path AUTH_DATA_PASS]
               [--parallelize]
               [-i INFRA_ID]
               infra_def

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--parallelize:`` (optional) parallelize processing instructions e.g. independent nodes are created parallel (default: sequential)
    * ``-i INFRA_ID:`` (optional) identifier of a previously built, existing infrastructure - if provided, occopus will reconfigure the existing infrastructure instead of building a new one. Use with caution! Occopus may build/destroy nodes based on the difference between the existing and the new infrastructure defined by ``infra_def``!
    * ``infra_def:`` file containing an infrastructure definition to be built

**Return type:**
    On successful finish it returns the identifier of the infrastructure. The identifier can be stored or listed by the occopus-maintain command.

occopus-destroy
===============

This command destroys an infrastructure including all of its nodes built previously by Occopus. No recover is possible.

**Usage:**

.. code:: bash

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
================

This command is capable of maintaining an infrastructure built by Occopus. Maintenance includes health checking, recovery and scaling. It can also list available infrastructure or can provide details on an infrastructure.

**Usage:**

.. code:: bash

 occopus-maintain [-h]
                  [--cfg CFG_PATH]
                  [--auth_data_path AUTH_DATA_PATH]
                  [--parallelize]
                  [-l|--list]
                  [-r|--report]
                  [-i INFRA_ID]
                  [-c|--cyclic]
                  [-t INTERVAL]
                  [-o|--output OUTPUT]
                  [-f|--filter FILTER]

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--parallelize:`` (optional) parallelize processing instructions e.g. independent nodes are created parallel (default: sequential)
    * ``-l, --list:`` (optional) list the built pieces of infrastructure
    * ``-r, --report:`` (optional) reports about an infrastructure
    * ``-i INFRA_ID:`` (optional) identifier of the infrastructure to maintain
    * ``-c, --cyclic:`` (optional) performs continuous maintenance
    * ``-t INTERVAL:`` (optional) specifies the time in seconds between maintenance sessions (default: 10)
    * ``-o OUTPUT:`` (optional) defines output file name for reporting on an infra (default: None)
    * ``-f FILTER:`` (optional) defines the nodename to be included in reporting (default: None)

.. _api-user_scalecommand:

occopus-scale
=============

This command registers scaling requests for a given node in an infrastructure. With scaling the instance count of a node can be increased or decreased by a given number. Scaling requests are handled and realized by the occopus-maintain command.

**Usage:**

.. code:: bash

 occopus-scale [-h]
               [--cfg CFG_PATH]
               [--auth_data_path AUTH_DATA_PATH]
               -i INFRA_ID
               -n|--node NODE
               [-c|--changescale CHANGESCALE]
               [-s|--setscale SETSCALE]
               [-f|--filter FILTER]

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``--auth_data_path AUTH_DATA_PATH:`` (optional) path to Occopus authentication file (default: None) if undefined, file named *auth_data.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``-i INFRA_ID:`` identifier of the infrastructure which contains the node to scale
    * ``-n NODE, --node NODE:`` name of the node to scale
    * ``-c CHANGESCALE, --changescale CHANGESCALE:`` positive/negative number expressing the direction and magnitude of scaling (positive: scale up; negative: scale down)
    * ``-s SETSCALE, --setscale SETSCALE:`` positive number expressing the number of nodes to scale to
    * ``-f FILTER, --filter FILTER:`` filter for selecting nodes for downscaling; filter can be nodeid or ip address (default: None)

occopus-import
==============

This command imports i.e. loads the node definitions from file to the database of Occopus.

.. important::

  Each time a node definition file changes, this command must be executed since Occopus takes node definitions from its database!

**Usage:**

.. code:: bash

 occopus-import [-h]
                [--cfg CFG_PATH]
                datafile

**Parameters:**
    * ``-h, --help:`` (optional) shows help message
    * ``--cfg CFG_PATH:`` (optional) path to Occopus config file (default: None) if undefined, file named *occopus_config.yaml* is searched at predefined locations, e.g. $HOME/.occopus
    * ``datafile:`` file containing node definition(s)

occopus-rest-service
====================

This command launches occopus as a web service. The occopus rest service can create, maintain, scale and destroy any infrastructure built by the service. This service provides a restful interface described by `REST API`_.

**Usage:**

.. code:: bash

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

.. _api-user_rest:

REST API
********

POST /infrastructures/
======================

Create a new infrastructure and returns the identifier of the infrastructure. The returned identifier can be used as ``infraid`` parameter in the infrastructure-related commands.

Requires an :ref:`infrastructure description <infradescription>` as POST data.

**Return type:**

.. code:: yaml

    {
        "infraid": "<infraid_in_uuid_format>"
    }

Example:

.. code:: bash

    curl -X POST http://127.0.0.1:5000/infrastructures/ --data-binary @my_infrastructure_description.yaml

GET /infrastructures/
=====================

List the identifier of infrastructures currently maintained by the service.

**Return type:**

.. code:: json

    {
        "infrastructures": [
            "<infraid_in_uuid_format_for_an_infrastructure>",
            "<infraid_in_uuid_format_for_another_infrastructure>"
            ]
    }

POST /infrastructures/(infraid)/scaledown/(nodename)/(nodeid)
=============================================================

Scales down a node in an infrastructure by destroying one of its instances specified.

**Parameters:**
    * ``infraid`` The identifier of the infrastructure.
    * `nodename:` The name of the node which is to be scaled down.
    * `nodeid:` The identifier of the selected instance.

**Return type:**

.. code:: json

    {
        "infraid": "<infraid>",
        "method": "scaledown",
        "nodeid": "<nodeid>",
        "nodename": "<nodename>"
    }

POST /infrastructures/(infraid)/scaleup/(nodename)/(int: count)
===============================================================

Scales up a node in an infrastructure by creating the specified number of instances of the node.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.
    * ``nodename:`` The name of the node to be scaled up.
    * ``count:`` The number of instances to be created.

**Return type:**

.. code:: json

    {
        "count": "<count>",
        "infraid": "<infraid>",
        "method": "scaleup",
        "nodename": "<nodename>"
    }

POST /infrastructures/(infraid)/scaleto/(nodename)/(int: count)
===============================================================

Scales a node in an infrastructure to a given count by creating or destroying instances of the node depending on the actual number of instances and the required number.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.
    * ``nodename:`` The name of the node to be scaled up.
    * ``count:`` The number of instances to scale the node to.

**Return type:**

.. code:: json

    {
        "count": "<count>",
        "infraid": "<infraid>",
        "method": "scaleto",
        "nodename": "<nodename>"
    }

POST /infrastructures/(infraid)/scaledown/(nodename)
====================================================

Scales up a node in an infrastructure by creating a new instance of the node.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.
    * ``nodename:`` The name of the node to be scaled up.

**Return type:**

.. code:: json

    {
        "count": 1,
        "infraid": "<infraid>",
        "method": "scaleup",
        "nodename": "<nodename>"
    }

POST /infrastructures/(infraid)/scaleup/(nodename)
==================================================

Scales up a node in an infrastructure by creating a new instance of the node.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.
    * ``nodename:`` The name of the node to be scaled up.

**Return type:**

.. code:: json

    {
        "count": 1,
        "infraid": "<infraid>",
        "method": "scaleup",
        "nodename": "<nodename>"
    }

POST /infrastructures/(infraid)/attach
======================================

Starts maintaining an existing infrastructure.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.

**Return type:**

.. code:: json

    {
        "infraid": "<infraid>"
    }

POST /infrastructures/(infraid)/detach
======================================

Stops maintaining an infrastructure.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.

**Return type:**

.. code:: json

    {
        "infraid": "<infraid>"
    }

POST /infrastructures/(infraid)/notify
======================================

Sets notification properties for an infrastructure.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure. Requires a notification description in JSON format as the POST data.

**Return type:**

.. code:: json

    {
        "infraid": "<infraid>",
    }

GET /infrastructures/(infraid)
==============================

Report the details of an infrastructure.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.

**Return type:**

.. code:: json

    {
        "<nodename>": {
            "instances": {
                "<nodeid>": {
                    "resource_address": "<ipaddress>",
                    "state": "<state>"
                }
            },
            "scaling": {
                "actual": "<current_number_of_instances>",
                "max": "<maximum_number_of_instances>",
                "min": "<minimum_number_of_instances>",
                "target": "<target_number_of_instances>"
            }
        },
    }


DELETE /infrastructures/(infraid)
=================================

Shuts down an infrastructure.

**Parameters:**
    * ``infraid:`` The identifier of the infrastructure.

**Return type:**

.. code:: json

    {
        "infraid": "<infraid>"
    }

.. _api-user_lib:

Python API
**********

Occopus provides a Python API which can be used to implement Occopus-based applications in a unified way. The API gives the possibility to utilise Occopus functionalities inside an application. To read about this possibility, please go to the :ref:`API section of the Developer guide<dev-api>`.

