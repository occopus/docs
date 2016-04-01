.. _createinfra:

Composing an infrastructure
===========================

.. _cloudinit site: https://cloudinit.readthedocs.org/en/latest

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

Abstract description of a node, which identifies a type of node a user may
include in an infrastructure. It is an abstract, *resource-independent*
definition of a class of nodes and can be stored in a repository.

This data structure does *not* contain information on how it can be
instantiated. It rather contains *what* needs to be instantiated, and under what *conditions*. It refers to one or more *implementations* that can be used
to instantiate the node. These implementations are described with :ref:`node
definition <usernodedefinition>` data structures.

To instantiate a node, its implementations are gathered first. Then, they are either filtered or one is selected by some brokering algorithm (currently: randomly).

    ``name``
        Uniquely identifies the node inside the infrastructure.

    ``type``
        The type of the node.

    ``filter`` (``dict``)
        Optional. Provides filtering among the available node definitions. The dictionary must define key-value pairs where keywords are originated from resource section of the node definitions. If unspecified, the one will be choosen among implementations.

    ``variables``
        Arbitrary mapping containing static node-level information:

        #. Inherited from the infrastructure.
        #. Overridden/specified in the node's description in the
           infrastructure description.

        The final list of variables is assembled by the Compiler

.. _usernodedefinition:

Node Definition
---------------

Describes an *implementation* of a :ref:`node <usernodedescription>`, a template that is required to instantiate a node. 

A node definition consists of 4 different sections:

#. ``resource`` Contains the definition of the resource and its attributes, like endpoint, image id, etc. The attributes to be defined are resource type dependent. There are 5 different resource plugins as mentioned in the :ref:`Supported Resources <clouds>` section, each one handles its own required and optional attributes. Possible attributes are defined in the :ref:`Resource section <userdefinitionresourcesection>`.

#. ``contextualisation`` Optional. Contains contextualisation information for the node to be instantiated. Possible attributes are defined in the :ref:`Contextualisation section <userdefinitioncontextualisationsection>`.

#. ``config_management`` Optional. Describes the configuration manager to be used and its required parameters. Currently, only chef is supported. Possible attributes are defined in the :ref:`Config management section <userdefinitionconfigmanagementsection>`.

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
    Regionname of for the ec2 cloud interface.
  ``image_id``
    The identifier of the image behind the ec2 cloud to be instantiated to realise a virtual machine.
  ``instance_type``
    The type of instance to be instantiated through EC2 when realising the virtual machine. This value refers to a flavour (e.g. m1.small) of the ec2 cloud. It determines the resources (CPU, memory, storage, networking) of the node.
  ``key_name``
    Optional. The name of the keypair to assign to the allocated virtual machine.
  ``security_group_ids``
    Optional. The list of security group IDs which should be assigned to the allocated virtual machine.
  ``subnet_id``
    Optional. The ID of the subnet which should be assigned to the allocated virtual machine.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authorisation file <authorisation>`.

Nova
^^^^
  ``type: nova`` 
    Selects the nova resource handler.
  ``endpoint``
    The endpoint (url) of the nova cloud interface.
  ``tenant_name``
    A container used to group or isolate resources on the cloud behind the nova interface.
  ``image_id``
    The identifier of the image behind the ec2 cloud to be instantiated to realise a virtual machine.
  ``flavor_name``
    The type of flavor to be instantiated through nova when realising this virtual machine. This value refers to a flavour (e.g. m1.small) of the nova cloud. It determines the resources (CPU, memory, storage, networking) of the node.
  ``server_name``
    Optional. The hostname of the instantiated virtual machine.
  ``key_name``
    Optional. The name of the keypair to be associated to the instance.
  ``security_groups``
    Optional. List of security groups to be associated to the instance.
  ``floating_ip``
    Optional. If defined (with any value), new floating IP address will be allocated and assigned for the instance.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authorisation file <authorisation>`.


OCCI
^^^^
  ``type: occi`` 
    Selects the occi resource handler. It requires the occi client to be installed locally.
  ``endpoint``
    The endpoint (url) of the occi cloud interface.
  ``os_tpl``
    The identifier of the VM image on the cloud.
  ``resource_tpl``
    The identifier of the instance type to be used to intantiate the VM image on the target cloud.
  ``public_key``
    Optional. The public ssh key to be deployed on the target virtual machine.
  ``link``
    Optional. List of compute or network resources to be attached to the VM. Using this option enables one to attach additional disk images or public networks to the VM.
  ``name``
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authorisation file <authorisation>`.

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
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authorisation file <authorisation>`.
      
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
    Optional. A user-defined name for this resource. Used in logging and can be referred to in the :ref:`authorisation file <authorisation>`.

.. _userdefinitioncontextualisationsection:

Contextualisation
~~~~~~~~~~~~~~~~~

In this section, the attributes (keywords) are listed and explained which can be used for the different contextualisation plugins.

Cloudinit
^^^^^^^^^
  ``type: cloudinit`` 
    Selects the cloudinit contextualisation plugin. Can be used with the following resource handlers: ec2, nova, occi.
  ``context_template``
    This section can contain a cloud init configuration template. It must follow the syntax of cloud-init. See the `Cloud-init website <cloudinit site>`_ for examples and details. Please note that Amazon AWS currently limits the length of this data in 16384 bytes.
  ``attributes``
    Optional. Any user-defined attributes. Used for specifying values of attributes in chef recepies.

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
    The endpoint (url) of the chef server containing the recepies.
  ``run_list``
    The list of recepies to be executed by chef on the node after startup.

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

  Optional. Health check includes testing against web services if urls are specified. Default is none. {{ip}} are substituted with the real ip of the node before health checking.

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

Examples
~~~~~~~~

**EC2 example**

.. code:: yaml

  'node_def:ec2_helloworld_node':
    -
        resource:
            type: ec2
            endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
            regionname: replace_with_regionname_of_your_ec2_interface
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
            key_name: replace_with_key_name_on_your_target_cloud
            security_group_ids:
                -
                    replace_with_security_group_id1_on_your_target_cloud
                -
                    replace_with_security_group_id2_on_your_target_cloud
            subnet_id: replace_with_subnet_id_on_your_target_cloud
        contextualisation:
            type: cloudinit
            context_template: !text_import
                url: file://cloud_init_helloworld.yaml

**OCCI example**

.. code:: yaml

  'node_def:occi_helloworld_node':
    -
        resource:
            type: occi
            endpoint: replace_with_endpoint_of_occi_interface_from_egi_appdb
            os_tpl: replace_with_occi_id_from_egi_appdb
            resource_tpl: replace_with_template_id_from_egi_appdb
            link:
                -
                    replace_with_public_network_identifier_or_remove
        contextualisation:
            type: cloudinit
            context_template: !text_import
                url: file://cloud_init_helloworld.yaml

**Chef example**

.. code:: yaml

  'node_def:ec2_chef_mysql_server_node':
    -
        resource:
            type: ec2
            endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
            regionname: replace_with_regionname_of_your_ec2_interface
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
            key_name: replace_with_key_name_on_your_target_cloud
            security_group_ids:
                -
                    replace_with_security_group_id1_on_your_target_cloud
                -
                    replace_with_security_group_id2_on_your_target_cloud
            subnet_id: replace_with_subnet_id_on_your_target_cloud
        contextualisation:
            type: cloudinit
            context_template: !text_import
                url: file://cloud_init_wordpress.yaml
            attributes:
                mysql:
                    server_root_password: '{{ variables.mysql_root_password }}'
                database_management:
                    database_name: '{{ variables.mysql_database_name }}'
                    dbuser_username: '{{ variables.mysql_dbuser_username }}'
                    dbuser_password: '{{ variables.mysql_dbuser_password }}'
        config_management:
            type: chef
            endpoint: replace_with_url_of_chef_server
            run_list:
                - recipe[database-setup::db]
        health_check:
            ping: true
            mysqldbs:
                - {name: '{{ variables.mysql_database_name }}',
                   user: '{{ variables.mysql_dbuser_username }}',
                   pass: '{{ variables.mysql_dbuser_password }}'}
  'node_def:ec2_chef_wordpress_node':
    -
        resource:
            type: ec2
            endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
            regionname: replace_with_regionname_of_your_ec2_interface
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
            key_name: replace_with_key_name_on_your_target_cloud
            security_group_ids:
                -
                    replace_with_security_group_id1_on_your_target_cloud
                -
                    replace_with_security_group_id2_on_your_target_cloud
            subnet_id: replace_with_subnet_id_on_your_target_cloud
        contextualisation:
            type: cloudinit
            context_template: !text_import
                url: file://cloud_init_wordpress.yaml
            attributes:
                wordpress:
                    db:
                        name: '{{ variables.mysql_database_name }}'
                        user: '{{ variables.mysql_dbuser_username }}'
                        pass: '{{ variables.mysql_dbuser_password }}'
        config_management:
            type: chef
            endpoint: replace_with_url_of_chef_server
            run_list:
                - recipe[wordpress]
        health_check:
            ping: true
            urls:
                - http://{{ip}}/wordpress

More examples can be found in the :ref:`tutorial section <tutorial>` of the User Guide.
