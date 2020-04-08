.. _createinfra:

Composing an infrastructure
===========================

In order to deploy an infrastructure, Occopus requires 
 #. description of the infrastructure
 #. definition of the individual nodes
  
The following section explains how the various descriptions must be formatted.

.. _infradescription:

Infrastructure Description
--------------------------

Dependency graph on :ref:`usernodedescription`-s.

The graph contains the following information:

    ``user_id``
        The identifier of the owner of the infrastructure instance.
    ``infra_name``
        The name of the infrastructure.
    ``nodes``
        List of node.
    ``dependencies``
        List of edge definitions. Each of these can be either

            - A pair (2-list) of node references.

            - A mapping containing:

                ``connection``
                    The pair (2-list) of node references.

                ``mappings``
                    List of attribute mappings. Each mapping can be a pair (2-list) of strings (attribute specifications, dotted strings permitted) or a mapping containing:

                    ``attributes``
                        The pair of attribute specifications.

                    ``synch``
                        Whether to synchronize on the availability of the source attribute.

                    ``**``
                        Anything else that is required by mediating services.

                ``**``
                    Anything else that is required by mediating services.

    ``variables``

        Arbitrary mapping containing infrastructure-wide information. This
        information is static (not parsed anywhere). Nodes will inherit these
        variables, but they may also override them.

The following example describes a two nodes infrastructure where B depends on A, i.e. B uses the service provided by A.

.. code:: yaml

    user_id: me
    infra_name: simple
    nodes: 
        - &A
            name: A
            type: mysql
        - &B
            name: B
            type: wordpress
    dependencies:
        - [ *B, *A ]

.. _usernodedescription:

Node Description
----------------

Abstract description of a node, which identifies a type of node a user may include in an infrastructure. It is an abstract, *resource-independent* definition of a class of nodes and can be stored in a repository.

This data structure does *not* contain information on how it can be instantiated. It rather contains *what* needs to be instantiated, and under what *conditions*. It refers to one or more *implementations* that can be used to instantiate the node. These implementations are described with :ref:`node definition <usernodedefinition>` data structures.

To instantiate a node, its implementations are gathered first. Then, they are filtered and one is selected by Occopus randomly.

    ``name``
        Name of node which uniquely identifies the node inside the infrastructure.

    ``type``
        The type of the node i.e. the node definition to be used when intantiating the node. If node definition exists for 'XXX' then use "type: XXX" to instantiate the implementation of node 'XXX'.

    ``filter`` (``dict``)

        .. code:: yaml
  
           filter:
              type: ec2
              regionname: ROOT
              instance_type: m1.small

        Optional. Provides filtering among the available implementations of a node definition specified for 'type'. The dictionary must define key-value pairs where keywords are originated from resource section of the node definitions. If unspecified or filtering results more than one implementations, one will be chosen by Occopus.

    ``scaling`` (``dict``)

        .. code:: yaml
  
           scaling:
              min: 1
              max: 3

        Optional. Keywords for scaling are ''min'' and ''max''. They specify how many instances of the node can have minimum (''min'') and maximum (''max'') in the infrastructure. At startup ''min'' number of instances of the node will be created. Default and minimal value for ''min'' is 1. Default value for ''max'' equals to ''min''. Both values are hardlimits, no modification of these limits are possible during infrastructure maintenance.

    ``variables``
        Arbitrary mapping containing static node-level information:

        #. Inherited from the infrastructure.
        #. Overridden/specified in the node's description in the
           infrastructure description.

        The final list of variables is assembled by Occopus.

.. _usernodedefinition:

Node Definition
---------------

Describes an *implementation* of a :ref:`node <usernodedescription>`, a template that is required to instantiate a node. 

A node definition consists of 4 different sections:

#. ``resource`` Contains the definition of the resource and its attributes, like endpoint, image id, etc. The attributes to be defined are resource type dependent. There are 5 different resource plugins as mentioned in the :ref:`Supported Resources <clouds>` section, each one handles its own required and optional attributes. Possible attributes are defined in the :ref:`Resource section <userdefinitionresourcesection>`.

#. ``contextualisation`` Optional. Contains contextualisation information for the node to be instantiated. Possible attributes are defined in the :ref:`Contextualisation section <userdefinitioncontextualisationsection>`.

#. ``config_management`` Optional. Describes the configuration manager to be used and its required parameters. Currently, chef and puppet are supported. Possible attributes are defined in the :ref:`Config management section <userdefinitionconfigmanagementsection>`.

#. ``health_check`` Optional. Can be specified if health of the node can be monitored. Default is ping to check network access. Possible attributes are defined in the :ref:`Health check section <userdefinitionhealthchecksection>`.

.. _userdefinitionresourcesection:

Resource 
~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for the different resource handlers.

EC2
^^^
  ``type: ec2`` 
    Selects the ec2 resource handler.
  ``endpoint``
    The endpoint (url) of the ec2 cloud interface.
  ``regionname``
    Region name of for the ec2 cloud interface.
  ``image_id``
    The identifier of the image behind the ec2 cloud to be instantiated to realize a virtual machine.
  ``instance_type``
    The instance type determines the characteristics (CPU, memory, storage, networking) of the VM created (e.g. m1.small).
  ``key_name``
    Optional. The name of the keypair to assign to the allocated virtual machine.
  ``security_group_ids``
    Optional. The list of security group IDs which should be assigned to the allocated virtual machine.
  ``subnet_id``
    Optional. The ID of the subnet which should be assigned to the allocated virtual machine.
  ``tags``
    Optional. List of key-value pairs of tags to be registered for the virtual machine.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.

Nova
^^^^
  ``type: nova`` 
    Selects the nova resource handler.
  ``endpoint``
    The endpoint (url) of the nova cloud interface.
  ``tenant_name``
    Optional. A container used to group or isolate resources on the cloud behind the nova interface. If this option is not specified, **project_id** and **user_domain_name** must be set.
  ``project_id``
    Optional. Specifies the ID of the project to connect to.
  ``user_domain_name``
    Optional. Specifies the name of the user domain. The default value of this attribute is "Default".
  ``network_id``
    Optional. Specifies the ID of the network to attach to the virtual machine.
  ``image_id``
    The identifier of the image on the cloud to be instantiated to realize a virtual machine.
  ``flavor_name``
    The type of flavor to be instantiated through nova when realizing this virtual machine. This value refers to a flavour of the nova cloud. It determines the resources (CPU, memory, storage, networking) of the node.
  ``server_name``
    Optional. The hostname of the instantiated virtual machine.
  ``key_name``
    Optional. The name of the keypair to be associated to the instance.
  ``security_groups``
    Optional. List of security groups to be associated to the instance.
  ``floating_ip``
    Optional. If defined (with any value), new floating IP address will be allocated and assigned for the instance.
  ``floating_ip_pool``
    Optional. If defined, also implies **floating_ip**, and specifies the name of the floating IP pool that should be used to allocate a new floating IP for the VM.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.


OCCI
^^^^
  ``type: occi`` 
    Selects the occi resource handler. It requires the occi client to be installed locally.
  ``endpoint``
    The endpoint (url) of the occi cloud interface.
  ``os_tpl``
    The identifier of the VM image on the cloud.
  ``resource_tpl``
    The identifier of the instance type to be used to instantiate the VM image on the target cloud.
  ``public_key``
    Optional. The public ssh key to be deployed on the target virtual machine.
  ``link``
    Optional. List of compute or network resources to be attached to the VM. Using this option enables one to attach additional disk images or public networks to the VM.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.

CloudBroker
^^^^^^^^^^^
  ``type: cloudbroker`` 
    Selects the cloudbroker resource handler.
  ``endpoint``
    The endpoint (url) of the cloudbroker REST API interface.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.
  ``description``
    Description of the virtual machine to be started by CloudBroker. This is a subsection containing further keywords. The available keywords in this section is documented in the `REST Web Service API documentation of CloudBroker <https://cola-prototype.cloudbroker.com/documents/CloudBrokerPlatform_RESTAPIUsageManual-2.3.13.0.pdf>`_ on page 49. However, the most important ones are detailed below.

    Obligatory keywords to be defined under `description` are as follows:

    ``deployment_id``
      Id of the deployment registered in CloudBroker. A deployment defines the cloud, the image, etc. to be instantiated.
    ``instance_type_id``
      Id of an instance type registered in CloudBroker and valid for the selected deployment. Instance type specifies the capabilities of the virtual machine to be instantiated.
    
    Important/suggested keywords to be defined under `description` are as follows:

    ``key_pair_id``
      The ID of the (ssh) key pair to be deployed on the virtual machine. Key pairs can be registered in the CloudBroker platform behind the 'Users'/'Key Pairs' menu after login. 
    ``opened_port``
      Determines if a port to be opened to the world. This is a list of numbers separated by comma.
      
  Example for a resource section including the description subsection:

  .. code:: yaml

     resource:
       type: cloudbroker
       endpoint: https://cola-prototype.cloudbroker.com/
       description:
         deployment_id: bcbdca8e-2841-45ae-884e-d3707829f548
         instance_type_id: c556cb53-7e79-48fd-ae71-3248133503ba
         key_pair_id: d865f75f-d32b-4444-9fbb-3332bcedeb75
         opened_port: 22,80

Docker
^^^^^^
  ``type: docker`` 
    Selects the docker resource handler.
  ``endpoint``
    The endpoint (url) of the docker/swarm interface.
  ``origin``
    The URL of an image or leave it empty and default will be set to dockerhub.
  ``image``
    The name of the image, e.g ubuntu, debian, mysql ..
  ``tag``
    Docker tag. (default = latest)
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.

CloudSigma
^^^^^^^^^^
  ``type: cloudsigma``
    Selects the cloudsigma resource handler.
  ``endpoint``
    The endpoint (URL) of the CloudSigma interface, e.g. https://zrh.cloudsigma.com/api/2.0
  ``libdrive_id``
    The UUID of the library drive image to use. After login to CloudSigma UI at https://zrh.cloudsigma.com/ui, select the menu ``Storage/Library``, select a library on page at https://zrh.cloudsigma.com/ui/#/library and use the uuid from the url of the selected item e.g. 40aa6ce2-5198-4e6b-b569-1e5e9fbaf488 for ``Ubuntu 15.10 (Wily)`` found at page https://zrh.cloudsigma.com/ui/#/library/40aa6ce2-5198-4e6b-b569-1e5e9fbaf488 .
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.
  ``description``
    Description of the virtual machine to be started in CloudSigma (e.g. CPU, memory, network, public key). This is a section containing further keywords. The available keywords in this section is defined in the `schema definition of CloudSigma VMs <https://cloudsigma-docs.readthedocs.io/en/2.14/servers.html#schema>`_ under the top-level keyword ``fields``.

    Obligatory keywords to be defined under `description` are as follows:

    ``cpu``
      Server's CPU Clock speed measured in MHz, e.g.: 2000
    ``mem``
      Server's Random Access Memory measured in bytes, e.g.: 1073741824 (for 1 GByte)
    ``vnc_password``
      VNC Password to connect to server, e.g. "secret"
    
    Example for a typical description section, using 2GHz CPU, 1GB RAM with public ip address.

    .. code:: yaml

       description:
         cpu: 2000
         mem: 1073741824
         vnc_password: the_password
         name: the_hostname
         pubkeys:
           -
             the_uuid_of_an_uploaded_keypair
         nics:
           -
             firewall_policy: the_uuid_of_a_predefined_firewall_policy
             ip_v4_conf:
               conf: dhcp
               ip: null
             runtime:
               interface_type: public

Azure
^^^^^
  ``type: azure``
    Selects the Azure resource handler.
  ``endpoint``
    The endpoint (url) of the Azure interface, e.g. https://management.azure.com
  ``resource_group``
    The resource group to allocate Azure resources in.
  ``location``
    The location where the resources should be allocated, e.g. francecentral.
  ``vm_size``
    The size of the VM to allocate, e.g. Standard_DS1_v2.
  ``publisher``
    The image publisher's name, e.g. Canonical.
  ``offer``
    The published name of the image, e.g. UbuntuServer.
  ``sku``
    The type of the OS, e.g. 16.04.0-LTS.
  ``version``
    The version of the image to use, e.g. latest.
  ``username``
    The name of the admin user to create on the VM.
  ``password``
    The password for the admin user.
  ``vnet_name``
    Optional. Name of the virtual network to use for the VM. If not specified, the Azure resource plugin will allocate a virtual network.
  ``nic_name``
    Optional. The name of the network interface to use for the VM. If not specified, the Azure resource plugin will allocate a network interface.
  ``subnet_name``
    Optional. The name of the subnet to use for the VM. If not specified, the Azure resource plugin will allocate a subnet.
  ``public_ip_needed``
    Optional. If specified with the value True, the Azure resource plugin will allocate a public IP address for the VM.


Collecting Resource Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following subsections detail how the string values (identifiers, settings, etc.) for the different attributes/keywords under the resource section of the node definition can be collected using the user interface of a particular resource.

.. toctree:: 

   collect_resource_attributes/amazon/index
   collect_resource_attributes/cloudsigma/index
   collect_resource_attributes/openstack_horizon/index
   collect_resource_attributes/cloudbroker/index
   

.. _userdefinitioncontextualisationsection:

Contextualisation
~~~~~~~~~~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for the different contextualisation plugins.

Cloudinit
^^^^^^^^^
  ``type: cloudinit`` 
    Selects the cloudinit contextualisation plugin. Can be used with the following resource handlers: ec2, nova, occi, cloudsigma, azure.
  ``context_template``
    This section can contain a cloud init configuration template. It must follow the syntax of cloud-init. See the `Cloud-init website <https://cloudinit.readthedocs.org/en/latest>`_ for examples and details. Please note that Amazon AWS currently limits the length of this data in 16384 bytes.
  ``attributes``
    Optional. Any user-defined attributes. Used for specifying values of attributes in chef recipes.

Docker
^^^^^^
  ``type: docker`` 
    Selects the docker contextualisation plugin. Can be used with the following resource handlers: docker.
  ``env``
    Environment variables to be passed to containers.
  ``command``
    Command to be executed inside the container once the container come to life.

.. _userdefinitioncontextualisationvariablesandmethodssection:

Contextualisation variables and methods
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contextualization plugins
^^^^^^^^^^^^^^^^^^^^^^^^^
In Occopus, each node can have contextualization which is processed at the startup phase during building the node. Occopus has a pluggable contextualization module, currently there are plugins called “cloudinit” and “docker”. The docker contextualization plugin can be used with docker containers to specify command, environment variables, etc. The cloudinit contextualization plugin can be used to specify user data passed to the cloud-init tool on the launched virtual machine. The required keywords for activating the cloudinit contextualization plugin is described in the manual.

Cloud-init plugin
^^^^^^^^^^^^^^^^^
The contextualization script for the cloudinit plugin can be dynamically updated with information Occopus has on the infrastructure and on its living nodes. The script may contain references to constants or even to methods which represent placeholders for dynamically resolvable strings. The script containing these placeholders are considered as template. Occopus performs the resolution of the template just before starting the virtual machine and passes it as user data to the Cloud API.

Jinja2 templating
^^^^^^^^^^^^^^^^^
For handling the contextualization script as template, Occopus uses Jinja2. Jinja2 is a designer-friendly full featured template engine. For detailed information on Jinja2, visit the website at `Jinja Desinger Documentation <http://jinja.pocoo.org/docs/latest/templates>`_. Since the content of the contextualization can be considered as a Jinja2 template, Jinja syntax can be used. The details of the syntax can be found on the Jinja webpage, however we provide a short summary for the simplest cases.

General rules
^^^^^^^^^^^^^
A template contains variables and/or expressions, which get replaced with values when a template is rendered. For variables and/or expressions a pair of double brackets (e.g. “{{foo}}” ) can be used, while statements are marked with bracket-percentage pair (e.g. “{% for item in seq %}” ).

How/where to define own variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Variables can be defined in Occopus in the infrastructure description in the node description or at global level. Variables can be defined to be valid only for a given node (see “foo” variable in the code below) or can be defined to be valid in the entire infrastructure (see “bar” variable in the code below).

myinfra.yaml:


 .. code::

  nodes:
      -
          name: mynode
          ...
          variables:
              foo: local
  variables:
      bar: global

How/where to refer to own variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In the text/yaml file containing the contextualisation/ user data, one may refer to predefined variables in the following way:

mycloudinit_context_file:


 .. code::

  write_files:
  - content: "foo: {{variables.foo}}\nbar: {{variables.bar}}\n"
    path: /tmp/myvars.txt:

As a result the cloud-init will create the following content:

/tmp/myvars.txt:


 .. code::

  foo: local
  bar: global

Enable/disable jinja syntax
^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you do not want Jinja to process a part of your text, put your text between the following two jinja commands. As a result Jinja will ignore to translate the text within this section.

 .. code::

  {% raw %}
  ...
  {% endraw %}

System level constants and methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Constants:
  ``infra_name``
    string containing the name of the infrastructure (as defined in infra description)
  ``infra_id``
    string containing the identifier of the infrastructure (generated by Occopus or user defined)
  ``name``
    string containing the name of the node (as defined in infra description)
  ``node_id``
    string containing the identifier of the node instance (uuid generated by Occopus)

Methods:
  ``getip``
    - Usage: 	getip(<name of node defined in infra description>)

    - Output: 	string containing an ip address of the (first) instance of the given node

    - Example:	getip(„master”), getip(variables.masterhostname)

  ``getprivip``
    - Usage: 	getprivip(<name of node defined in infra description>)

    - Output: 	string containing a private ip address of the (first) instance of the given node

    - Example:	getprivip(„master”), getprivip(variables.masterhostname)

  ``getipall``
    -  Usage: 	getipall(<name of node defined in infra description>)

    - Output: 	string list containing ip addresses of the instances of the given node

    - Example:	getipall(„master”), getipall(variables.masterhostname)

  ``cut``
    - Usage: 	cut(<string to be sliced>,<startindex>,<endindex>)

    - Output: 	substring of the given string between the indexes

    - Example:	cut(infra_id,0,7)

  ``cmd``
    - Usage: 	cmd('command with options')

    - Output: 	string returned by the command

    - Example:	cmd('curl -X GET http://localhost/message.txt'), cmd('cat /etc/hosts')

.. _userdefinitionconfigmanagementsection:

Config management
~~~~~~~~~~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for the different config manager plugins.

Chef
^^^^
  ``type: chef`` 
    Selects chef as config manager.
  ``endpoint``
    The endpoint (url) of the chef server containing the recipes.
  ``run_list``
    The list of recipes to be executed by chef on the node after startup.

Puppet-solo
^^^^^^^^^^^
  ``type: puppet_solo`` 
    Selects puppet (server-free version) as config manager.
  ``manifests``
    The location (url) of the puppet manifest files to be deployed.
  ``modules``
    The list module names to be of deployed by puppet.
  ``attributes``
    List of attribute-value pairs defining the values of the attributes.

.. _userdefinitionhealthchecksection:

Health-check
~~~~~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for to specify the way of health monitoring of the node.

Ping
^^^^
  .. code:: yaml

     ping: True

  Optional. Health check includes ping test against the node if turned on. Default is on. 

Ports
^^^^^
  .. code:: yaml
  
     ports:
         - 22
         - 1234

  Optional. Health check includes testing against open ports if list of ports are specified. Default is none.

Urls
^^^^
  .. code:: yaml
  
     urls:
         - http://{{ip}}:5000/myserviceOne
         - http://{{ip}}:6000/myserviceTwo

  Optional. Health check includes testing against web services if urls are specified. Default is none. The ``{{ip}}`` in the url means the ip address of the node being specified.

MysqlDBs
^^^^^^^^
  .. code:: yaml
  
     mysqldbs:
         - { name: 'mydbname1', user: 'mydbuser1', pass: 'mydbpass1' }
         - { name: 'mydbname2', user: 'mydbuser2', pass: 'mydbpass2' }

  Optional. Health check includes testing available and accessible mysql database connection if name, user, pass triples are specified. Default is none. If specified mysql database connecticity check is performed with the given parameters.

Timeout
^^^^^^^
  .. code:: yaml
  
     timeout: 600

  Optional. Specifies a period in seconds after which continuous failure results in the node considered as failed. The current protocol in Occopus is to restart failed nodes. Default is 600.

.. _userdefinition_multinode:

Multiple node implementations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When creating node definitions, you can create multiple implementations for the
same node. These implementations can differ in any parameter listed in the
sections before, including but not
limited to: resource backend, image id, instance type, contextualization,
configuration management, health-check services used, etc.
To create multiple implementations, just list them using hyphens. Make sure to
watch for the indentation of the blocks.

The following example shows a node definition with multiple different
implementations.

.. code:: yaml

    'node_def:example_node':
        -
            resource:
                name: my_opennebula_ec2
                type: ec2
                endpoint: my_opennebula_endpoint
                ...
            ...
            config_management:
                type: chef
                ...
        -
            resource:
                name: my_aws_ec2
                type: ec2
                endpoint: my_aws_endpoint
                ...
            ...
        -
            resource:
                name: my_nova
                type: nova
                endpoint: my_nova_endpoint
                ...
            ...
            config_management:
                type: puppet_solo
                ...
            ...

If there are multiple implementations for a node definition, you can filter them
in the :ref:`Node description <usernodedescription>`, in the
:ref:`Infrastructure description <infradescription>` file. Occopus will
automatically select an available implementation to launch from those fulfilling the
filtering parameters.

Examples
~~~~~~~~

Examples can be found in the :ref:`tutorial section <tutorial>` of the User Guide.

