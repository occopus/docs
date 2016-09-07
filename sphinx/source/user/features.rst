.. _features:

Features
========

Wide range of supported resources
---------------------------------

Occopus can be used with a wide variety of different technologies including most
major cloud providers.
:ref:`See the full list of supported technologies <clouds>`

Hybrid cloud support
--------------------

Use Occopus to deploy the nodes of your infrastucture into different clouds,
making it more flexible, versatile and error-proof.

Multiple configuration tool support
-----------------------------------

Use Chef, Cloud-init, pre-defined images, or any combination of these in the
same infrastructure

Different usage possibilities
-----------------------------

Use Occopus via a CLI, as a REST service, or import it as a library into your
own application.
:ref:`See the detailed description in the concept section <concept>`

Simple YAML format
------------------

Occopus uses YAML files for node definitions and infrastructure descriptions,
making them simple, human-readable and easy-to-learn.
:ref:`Jump to the node definitions <usernodedefinition>`
:ref:`Jump to the infrastructure descriptions <infradescription>`

Double layered schema-checking
------------------------------

* Syntactic schema-check: Occopus validates if your files are valid YAML format
* Semantic schema-check: Occopus validates the content of your node-definition
  and infrastructure-description files, checking for missing or invalid keys

Dynamic reconfiguration
-----------------------

Make changes to your infrastructures on the fly with a single command. 
After updating the infrastructure description in the datastore using :ref:`occopus-build command <api-user_buildcommand>`, Occopus will automatically reconfigure the nodes of running infrastructures to match the new definitions.
:ref:`See the extended documentation of how to reconfigure an infrastructure <>`

Health-checking
---------------

Occopus provides a wide variety of tools to check a node's status, including
port-, URL- and database-availability.
:ref:`See the full detailed list of health-checking tools <userdefinitionhealthchecksection>`

Auto-healing
------------

By monitoring the states of the nodes, Occopus can automatically detect failed
nodes, and rebuild them.

Manual scaling
--------------

Scale your nodes up or down anytime by a single command
:ref:`Jump to the scale command <api-user_scalecommand>`

Multiple node implementations
-----------------------------

Define multiple implementations to a node-type and use different backends, images,
tools and variables in them. You can filter the available implementations in the
infrastructure description, and occopus will select an implementations from
those which fulfill the filtering parameters
:ref:`Jump to Multiple implementations section <>`
:ref:`Jump to node type filtering section <>`

Authenticator-selection
-----------------------

Occopus can automatically select which authentication-data to use based on the
resource and config-management tool used on a given node. The selection can be
based on any parameter, including name, type, image-id, etc.
:ref:`Jump to Authentication section <authentication>`

Easily extensible architecture
------------------------------

Occopus was created with extensibility and flexibility in mind - New modules for
resource-handlers, configuration-managemet tools, additional schema-checking
rules or health-checking tools can easily be implemented and added without
modifying other components.

