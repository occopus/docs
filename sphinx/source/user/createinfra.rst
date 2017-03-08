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
    The identifier of the image behind the ec2 cloud to be instantiated to realize a virtual machine.
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
    The endpoint (url) of the cloudbroker interface.
  ``software_id``
    The ID of the CloudBroker Software to use.
  ``executable_id``
    The ID of the CloudBroker Executable to use.
  ``resource_id``
    The ID of the CloudBroker Resource (cloud) to use.
  ``region_id``
    The ID of the CloudBroker Region (cloud region) to use.
  ``instance_type_id``
    The ID of the CloudBroker Instance to use.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authentication file <authentication>` to distinguish authentication to be applied among resources having the same type.
      
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
  ``network_mode``
    One of 'bridge', 'none', 'container:<name|id>', 'host' or an existing network.
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
  ``description``
    Description of the virtual machine to be started in CloudSigma (e.g. CPU, memory, network, public key). This is a section containing further keywords. The available keywords in this section is defined in the `schema definition of CloudSigma VMs <https://cloudsigma-docs.readthedocs.io/en/2.14/servers.html#schema>`_ under the top-level keyword ``fields``.

    Obligatory keywords to be defined under `description` are as follows:

    ``cpu``
      Server's CPU Clock speed measured in MHz, e.g.: 2048
    ``mem``
      Server's Random Access Memory measured in bytes, e.g.: 1073741824 (for 1 GByte)
    ``vnc_password``
      VNC Password to connect to server, e.g. "secret"
    
    Example for a typical description section, using 2GHz CPU, 1GB RAM with public ip address.

    .. code:: yaml

       description:
         cpu: 2048
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

Collecting Resource Attributes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following subsections detail how the string values (identifiers, settings, etc.) for the different attributes/keywords under the resource section of the node definition can be collected using the user interface of a particular resource.

.. toctree:: 

   collect_resource_attributes/amazon/index
   collect_resource_attributes/cloudsigma/index
   collect_resource_attributes/openstack_horizon/index
   

.. _userdefinitioncontextualisationsection:

Contextualisation
~~~~~~~~~~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for the different contextualisation plugins.

Cloudinit
^^^^^^^^^
  ``type: cloudinit`` 
    Selects the cloudinit contextualisation plugin. Can be used with the following resource handlers: ec2, nova, occi, cloudsigma.
  ``context_template``
    This section can contain a cloud init configuration template. It must follow the syntax of cloud-init. See the `Cloud-init website <https://cloudinit.readthedocs.org/en/latest>`_ for examples and details. Please note that Amazon AWS currently limits the length of this data in 16384 bytes.
  ``attributes``
    Optional. Any user-defined attributes. Used for specifying values of attributes in chef recipes.

Cloudbroker
^^^^^^^^^^^
  ``type: cloudinit`` 
    Selects the cloudbroker contextualisation plugin. Can be used with the following resource handlers: cloudbroker.
  ``template_files``
    A list of file templates. These templates will be actualized, and passed as input files to the jobs instantiated. The following child attributes must be defined:
      ``file_name``
          The name of the file. This name will be used to upload the actualized content.
      ``content_template``
          This section contains the template.
  ``files``
    A list of files. The files listed under this section will not be resolved i.e. their content will be used without any modification.

Docker
^^^^^^
  ``type: docker`` 
    Selects the docker contextualisation plugin. Can be used with the following resource handlers: docker.
  ``env``
    Environment variables to be passed to containers.
  ``command``
    Command to be executed inside the container once the container come to life.

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

