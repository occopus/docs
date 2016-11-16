.. _features:

Features
========

**Wide range of supported resources**

| Occopus can be used with a wide variety of different technologies including most
  major cloud providers.
| :ref:`List of supported technologies <clouds>`

**Hybrid cloud support**

| Occopus can be used to deploy the nodes of your infrastucture into different clouds,
  making it more flexible, versatile and error-proof. To use different
  clouds/backends, simply set the desired type in the resource section of the node
  definition.
| :ref:`Resource section of node definition <userdefinitionresourcesection>`

**Multiple configuration tool support**

Use Chef, Cloud-init, pre-defined images, or any combination of these in the
same infrastructure. Occopus has access to various configuration and contextualization methods:

* You can use pre-defined images in the resource section of the node definition 
 
  * :ref:`Resource section of node definition <userdefinitionresourcesection>`

* You can use cloud-init as a contextualisation tool 
  
  * :ref:`Contextualisation section of node definition <userdefinitioncontextualisationsection>`

* Occopus has support for configuration management tools. Currently, Chef is supported.

  * :ref:`Using Chef in node definition <userdefinitionconfigmanagementsection>`

  * :ref:`Demo infrastructures using chef <tutorial-advanced>`

**Different usage possibilities**

| Use Occopus via a CLI, as a REST service, or import it as a library into your
  own application. 
| :ref:`See the detailed description in the concept section <concept>`

**Simple YAML format**

| Occopus uses YAML files for node definitions and infrastructure descriptions, 
  making them simple, human-readable and easy-to-learn.
| :ref:`Node definitions <usernodedefinition>`
| :ref:`Infrastructure descriptions <infradescription>`

**Schema checking**

Both, infra description and node definition files are analysed and validated by 
Occopus by searching for missing or invalid sections and attributes. This helps
users to avoid creating syntactically wrong descriptor files.

**Dynamic reconfiguration**

Make changes to your infrastructures on the fly with a single command. 
Modify the infrastructure description file the way you want - add and remove
nodes, set new paramateres (e.g. scaling) and variables for your nodes and your
infrastructure and modify the dependency graph as you wish.
After updating the infrastructure description in the datastore using 
:ref:`occopus-build command <api-user_buildcommand>`, Occopus will automatically reconfigure the nodes of running infrastructures to match the new definitions.

**Health checking**

| Occopus supports health checking primitives to check if a node is still operating.
  These primitives are network availability of the node (ping), checking the connectivity 
  of a certain port (port access), checking the responsiveness of a web service (url checking) or
  checking the connectivity of a mysql database (mysql access).
| :ref:`Health checking primitives <userdefinitionhealthchecksection>`

**Auto healing***

Occopus monitors the states of the nodes by applying the primitives configured 
by health-checking for each node. Once, a node does not fails on health-checking,
it is considered as fail node, Occopus destroys and rebuilds it.

**Manual scaling**

| Scaling up or down any nodes in the infrastructure is supported. Occopus can 
  launch multiple instances of a certain node, however the infrastructure itself 
  must be built in a way to handle scaling events.
| :ref:`Scaling commands <api-user_scalecommand>`
| :ref:`Scaling limits in node description <usernodedescription>`

**Multiple node implementations**

| Occopus supports defining multiple implementations for a node (type) and
  utilise different backends, images, tools and variables in them. You can 
  filter the available implementations in the infrastructure description, 
  and occopus will select an implementation from the remaining ones.
| :ref:`Multiple node implementations <userdefinition_multinode>`
| :ref:`Node type filtering in infrastructure description <usernodedescription>`

**Multiple authenticators**

| Occopus can handle multiple authenticators during building an infrastructure 
  on multiple resource. Multiple resources may have different authenticators and
  authentication procedures. Occopus supports defining authenticators and selecting
  one of them for a certain resource. The selection can be based on any parameter of
  a resource handler, including name, type, image-id, etc.
| :ref:`Description of authentication <authentication>`

**Extensible architecture**

Occopus was created with extensibility and flexibility in mind - New modules for
resource-handlers, configuration-managers, additional schema-checker
rules or health-checking primitives can easily be implemented and added without
modifying other components.



