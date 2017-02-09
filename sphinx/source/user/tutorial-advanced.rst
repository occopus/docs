.. _tutorial-advanced:

Advanced
========

In this section more advanced solutions will be shown. The examples will introduce complex infrastructures or will introduce more complex features of the Occopus tool.

Please, note that the following examples require a properly configured Occopus, therefore we suggest to continue this section if you already followed the instructions written in the :ref:`Installation <installation>` section.

Chef-Apache2
~~~~~~~~~~~~
This tutorial uses Chef as a configuration management tool to deploy a one-node infrastructure containing an Apache2 web server.

**Features**

 - using Chef as a configuration management tool to deploy services
 - assembling the run-lists of the chef-clients on the nodes

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, OCCI, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - accessing the Chef server as user by Occopus (user name, user key)
 - accessing the Chef server as client by the nodes (validator client name, validator client key)
 - ``apache2`` community recipe (available at Chef Supermarket) and its dependencies uploaded to target Chef Server

**Download**

You can download the example as `tutorial.examples.ec2-chef-apache2 <../../examples/ec2-chef-apache2.tgz>`_ .

.. note::

   In this tutorial, we will use ec2 cloud resources (based on our ec2 tutorials in the basic tutorial section). However, feel free to use any Occopus-compatible cloud resource for the nodes - you can even use different types of resources for each node.

**Steps**

#. Edit ``nodes/node_definitions.yaml``. Configure the ``resource`` section as seen in the basic tutorials. For example, if you are using an ``ec2`` cloud, you have to set the following:

   - ``endpoint`` is an url of an EC2 interface of a cloud (e.g. `https://ec2.eu-west-1.amazonaws.com`).
   - ``regionname`` is the region name within an EC2 cloud (e.g. `eu-west-1`).
   - ``image_id`` is the image id (e.g. `ami-12345678`) on your EC2 cloud. Select an image containing a base os installation with cloud-init support!
   - ``instance_type`` is the instance type (e.g. `m1.small`) of your VM to be instantiated.
   - ``key_name``  optionally specifies the keypair (e.g. `my_ssh_keypair`) to be deployed on your VM.
   - ``security_group`` optionally specifies security settings (you can define multiple security groups in the form of a list, e.g. `sg-93d46bf7`) of your VM.
   - ``subnet_id`` optionally specifies subnet identifier (e.g. `subnet-644e1e13`) to be attached to the VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:ec2_chef_apache2_node':
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
             ...
  
#. Edit ``nodes/node_definitions.yaml``. Configure the ``config_management``. Set the ``endpoint`` to the url of your Chef Server.

   .. code::

     'node_def:ec2_chef_apache2_node':
         -
             resource:
                ...
             ...
             config_management:
                type: chef
                endpoint: replace_with_url_of_chef_server
                run_list:
                    - recipe[apache2]
             ...

#. Edit the ``nodes/cloud_init_chef.yaml`` contextualization file. Set the following attributes:

   - ``server_url`` is the url of your Chef Server (e.g. `"https://chef.yourorg.com:4000"`).
   - ``validation_name`` the name of the validator client through which nodes register to your chef server.
   - ``validation_key`` the public key belonging to the validator client.

   .. code::
 
      Example:
      
      validation_name: "yourorg-validator"
      validation_key: |
          -----BEGIN RSA PRIVATE KEY-----
          YOUR-ORGS-VALIDATION-KEY-HERE
          -----END RSA PRIVATE KEY-----

   .. important::

      Make sure you do not mix the ``validator client`` with ``user`` belonging to the Chef Server.

   .. code::

     ...
     chef:
        install_type: omnibus
        omnibus_url: "https://www.opscode.com/chef/install.sh"
        force_install: false
        server_url: "replace_with_your_chef_server_url"
        environment: {{infra_id}}
        node_name: {{node_id}}
        validation_name: "replace_with_chef_validation_client_name"
        validation_key: |
            replace_with_chef_validation_client_key
     ...

   .. important::

     Do not modify the value of "environment" and "node_name" attributes!

   .. note::

     For further explanation of the keywords, please read the `cloud-init documentation <http://cloudinit.readthedocs.org/en/latest/topics/examples.html#install-and-run-chef-recipes>`_!

#. Make sure your authentication information is set correctly in your authentication file. You must set your authentication data for the ``resource`` you would like to use, as well as the authentication data for the ``config_management`` section. Setting authentication information for both is described :ref:`here <authentication>`.

   .. important::

      Do not forget to set your Chef credentials!

#. Load the node definitions into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-chef-apache2.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

      List of nodes/ip addresses:
      apache2:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

Chef-Wordpress
~~~~~~~~~~~~~~
This tutorial uses Chef as a configuration management tool to deploy a two-node infrastructure containing a MySQL server node and a Wordpress node. The Wordpress node will connect to the MySQL database.

**Features**

 - using Chef as a configuration management tool to deploy services
 - passing variables to Chef through Occopus
 - assembling the run-lists of the chef-clients on the nodes
 - checking MySQL database availability on a node
 - checking url availability on a node

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, OCCI, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - accessing the Chef server as user by Occopus (user name, user key)
 - accessing the Chef server as client by the nodes (validator client name, validator client key)
 - ``wordpress`` community recipe (available at Chef Supermarket) and its dependencies uploaded to target Chef Server
 - ``database-setup`` recipe (provided in example package at Download) uploaded to target Chef server

**Download**

You can download the example as `tutorial.examples.ec2-chef-wordpress <../../examples/ec2-chef-wordpress.tgz>`_ .

.. note::

   In this tutorial, we will use ec2 cloud resources (based on our ec2 tutorials in the basic tutorial section). However, feel free to use any Occopus-compatible cloud resource for the nodes - you can even use different types of resources for each node.

**Steps**

#. Edit ``nodes/node_definitions.yaml``. For each node, configure the ``resource`` section as seen in the basic tutorials. For example, if you are using an ``ec2`` cloud, you have to set the following:

   - ``endpoint`` is an url of an EC2 interface of a cloud (e.g. `https://ec2.eu-west-1.amazonaws.com`).
   - ``regionname`` is the region name within an EC2 cloud (e.g. `eu-west-1`).
   - ``image_id`` is the image id (e.g. `ami-12345678`) on your EC2 cloud. Select an image containing a base os installation with cloud-init support!
   - ``instance_type`` is the instance type (e.g. `m1.small`) of your VM to be instantiated.
   - ``key_name``  optionally specifies the keypair (e.g. `my_ssh_keypair`) to be deployed on your VM.
   - ``security_group`` optionally specifies security settings (you can define multiple security groups in the form of a list, e.g. `sg-93d46bf7`) of your VM.
   - ``subnet_id`` optionally specifies subnet identifier (e.g. `subnet-644e1e13`) to be attached to the VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:ec2_chef_mysql_node':
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
             ...
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
             ...
  
#. Edit ``nodes/node_definitions.yaml``. For each node, configure the ``config_management``. Set the ``endpoint`` to the url of your Chef Server.

   .. code::

     'node_def:ec2_chef_mysql_node':
         -
             resource:
                ...
             ...
             config_management:
                type: chef
                endpoint: replace_with_url_of_chef_server
                run_list:
                    - recipe[database-setup::db]
             ...
     'node_def:ec2_chef_wordpress_node':
         -
             resource:
                ...
             ...
             config_management:
                type: chef
                endpoint: replace_with_url_of_chef_server
                run_list:
                    - recipe[wordpress]
             ...

#. Edit the ``nodes/cloud_init_chef.yaml`` contextualization file. Set the following attributes:

   - ``server_url`` is the url of your Chef Server (e.g. `"https://chef.yourorg.com:4000"`).
   - ``validation_name`` the name of the validator client through which nodes register to your chef server.
   - ``validation_key`` the public key belonging to the validator client.

   .. code::
 
      Example:
      
      validation_name: "yourorg-validator"
      validation_key: |
          -----BEGIN RSA PRIVATE KEY-----
          YOUR-ORGS-VALIDATION-KEY-HERE
          -----END RSA PRIVATE KEY-----

   .. important::

      Make sure you do not mix the ``validator client`` with ``user`` belonging to the Chef Server.

   .. code::

     ...
     chef:
        install_type: omnibus
        omnibus_url: "https://www.opscode.com/chef/install.sh"
        force_install: false
        server_url: "replace_with_your_chef_server_url"
        environment: {{infra_id}}
        node_name: {{node_id}}
        validation_name: "replace_with_chef_validation_client_name"
        validation_key: |
            replace_with_chef_validation_client_key
     ...

   .. important::

     Do not modify the value of "environment" and "node_name" attributes!

   .. note::

     For further explanation of the keywords, please read the `cloud-init documentation <http://cloudinit.readthedocs.org/en/latest/topics/examples.html#install-and-run-chef-recipes>`_!

#. Edit ``infra-chef-wordpress.yaml``. Set your desired root password, database name, username, and user password for your MySQL database in the variables section. These parameters will be applied when creating the mysql database.

   .. code::

     ...
     variables:
        mysql_root_password: replace_with_database_root_password
        mysql_database_name: replace_with_database_name
        mysql_dbuser_username: replace_with_database_username
        mysql_dbuser_password: replace_with_database_user_password

#. Make sure your authentication information is set correctly in your authentication file. You must set your authentication data for the ``resource`` you would like to use, as well as the authentication data for the ``config_management`` section. Setting authentication information for both is described :ref:`here <authentication>`.

   .. important::

      Do not forget to set your Chef credentials!

#. Load the node definitions into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-chef-wordpress.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

      List of nodes/ip addresses:
      mysql-server:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      wordpress:
          192.168.xxx.xxx (894fe127-28c9-4c8f-8c5f-2f120c69b9c3)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

PuppetSolo-Wordpress
~~~~~~~~~~~~~~~~~~~~
This tutorial uses Puppet as a configuration management tool in a server-free mode to deploy a two-node infrastructure containing a MySQL server node and a Wordpress node. The Wordpress node will connect to the MySQL database.

**Features**

 - using server-free Puppet as a configuration management tool to deploy services
 - defining puppet manifests and modules
 - passing attributes to Puppet through Occopus
 - checking MySQL database availability on a node
 - checking url availability on a node

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, OCCI, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - ``wordpress-init`` puppet recipe (provided in example package at Download) 
 - ``mysql-init`` puppet recipe (provided in example package at Download)

**Download**

You can download the example as `tutorial.examples.ec2-puppet-solo-wordpress <../../examples/ec2-puppet-solo-wordpress.tgz>`_ .

.. note::

   In this tutorial, we will use ec2 cloud resources (based on our ec2 tutorials in the basic tutorial section). However, feel free to use any Occopus-compatible cloud resource for the nodes - you can even use different types of resources for each node.

**Steps**

#. Edit ``nodes/node_definitions.yaml``. For each node, configure the ``resource`` section as seen in the basic tutorials. For example, if you are using an ``ec2`` cloud, you have to set the following:

   - ``endpoint`` is an url of an EC2 interface of a cloud (e.g. `https://ec2.eu-west-1.amazonaws.com`).
   - ``regionname`` is the region name within an EC2 cloud (e.g. `eu-west-1`).
   - ``image_id`` is the image id (e.g. `ami-12345678`) on your EC2 cloud. Select an image containing a base os installation with cloud-init support!
   - ``instance_type`` is the instance type (e.g. `m1.small`) of your VM to be instantiated.
   - ``key_name``  optionally specifies the keypair (e.g. `my_ssh_keypair`) to be deployed on your VM.
   - ``security_group`` optionally specifies security settings (you can define multiple security groups in the form of a list, e.g. `sg-93d46bf7`) of your VM.
   - ``subnet_id`` optionally specifies subnet identifier (e.g. `subnet-644e1e13`) to be attached to the VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:ec2_puppet_solo_mysql_node':
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
             ...
     'node_def:ec2_puppet_solo_wordpress_node':
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
             ...
  
#. Edit ``infra-puppet-solo-wordpress.yaml``. Set your desired root password, database name, username, and user password for your MySQL database in the variables section. These parameters will be applied when creating the mysql database and also used by wordpress node when connecting to mysql.

   .. code::

     ...
     variables:
        mysql_root_password: replace_with_database_root_password
        mysql_database_name: replace_with_database_name
        mysql_dbuser_username: replace_with_database_username
        mysql_dbuser_password: replace_with_database_user_password

#. Load the node definitions into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-puppet-solo-wordpress.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

      List of nodes/ip addresses:
      mysql-server:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      wordpress:
          192.168.xxx.xxx (894fe127-28c9-4c8f-8c5f-2f120c69b9c3)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

OCCI-DockerSwarm
~~~~~~~~~~~~~~~~
This tutorial sets up a complete Docker infrastructure with Swarm, Docker and Consul software components. It contains a head node and predefined number of worker nodes. The worker nodes receive the ip of the head node and attach to the head node to form a cluster. Finally, the docker cluster can be used with any standard tool talking the docker protocol (on port 2375).

**Features**

 - creating two types of nodes through contextualisation
 - passing ip address of a node to another node
 - using the occi resource handler
 - utilising health check against a predefined port
 - using parameters to scale up worker nodes

**Prerequisites**

 - accessing an OCCI cloud through its OCCI interface (endpoint, X.509 VOMS proxy)
 - target cloud contains an Ubuntu 14.04 image with cloud-init support (os_tpl, resource_tpl)
 - properly installed occi command-line client utility (occi command)

**Download**

You can download the example as `tutorial.examples.occi-dockerswarm <../../examples/occi-dockerswarm.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit ``nodes/node_definitions.yaml``. For ``occi_dockerswarm_head_node`` and ``occi_dockerswarm_worker_node`` nodes set the followings in their ``resource`` section:

   - ``endpoint`` is an url of an Occi interface of a cloud (e.g. `https://carach5.ics.muni.cz:11443`) stored in the EGI AppDB.
   - ``os_tpl`` is an image identifier for Occi (e.g. `os_tpl#uuid_egi_ubuntu_server_14_04_lts_fedcloud_warg_131`) stored in the EGI AppDB. Select an image containing an Ubuntu 14.04 operating system with cloud-init support! Please, note that the cloud-init script in this example depends on Ubuntu 14.04!
   - ``resource_tpl`` is the instance type in Occi (e.g. `http://fedcloud.egi.eu/occi/compute/flavour/1.0#medium`) stored in the EGI AppDB.
   - ``link``  specifies the network (e.g. `https://carach5.ics.muni.cz:11443/network/24` and/or storage resources to be attached to the VM.
   - ``public_key`` specifies the path to your ssh public key (e.g. `/home/user/.ssh/authorized_keys`) to be deployed on the target VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. hint::

      You can use the values shown above as examples to have an operational docker swarm cluster or find other sites and settings in the EGI AppDB!

   .. code::

     'node_def:occi_dockerswarm_head_node':
         -
             resource:
                 type: occi
                 endpoint: replace_with_endpoint_of_occi_interface_from_egi_appdb
                 os_tpl: replace_with_occi_id_from_egi_appdb
                 resource_tpl: replace_with_template_id_from_egi_appdb
                 link:
                     -
                         replace_with_public_network_identifier_or_remove
                 public_key: replace_with_path_to_your_ssh_public_key
             ...
     'node_def:occi_dockerswarm_worker_node':
         -
             resource:
                 type: occi
                 endpoint: replace_with_endpoint_of_occi_interface_from_egi_appdb
                 os_tpl: replace_with_occi_id_from_egi_appdb
                 resource_tpl: replace_with_template_id_from_egi_appdb
                 link:
                     -
                         replace_with_public_network_identifier_or_remove
                 public_key: replace_with_path_to_your_ssh_public_key

#. Make sure your authentication information is set correctly in your authentication file. You must set the path of your VOMS proxy in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Load the node definition for ``occi_dockerswarm_head_node`` and ``occi_dockerswarm_worker_node`` nodes into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition (file) changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Update the number of worker nodes if necessary. For this, edit the ``infra-docker-swarm.yaml`` file and modify the ``min`` parameter under the ``scaling`` keyword. Currently, it is set to ``2``.

   .. code::

     - &W
         name: worker
         type: occi_dockerswarm_worker_node
         scaling:
             min: 2
         variables:
             head_node: head

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-docker-swarm.yaml

   .. note::

      It may take a few minutes until the services on the head node come to live. Please, be patient!

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

     List of nodes/ip addresses:
     head:
       147.228.xxx.xxx (dfa5f4f5-7d69-432e-87f9-a37cd6376f7a)
     worker:
       147.228.xxx.xxx (cae40ed8-c4f3-49cd-bc73-92a8c027ff2c)
       147.228.xxx.xxx (8e255594-5d9a-4106-920c-62591aabd899)
     77cb026b-2f81-46a5-87c5-2adf13e1b2d3

#. Check the result by submitting docker commands to the docker head node!

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 77cb026b-2f81-46a5-87c5-2adf13e1b2d3



Autoscaling-DataAvenue
~~~~~~~~~~~~~~~~~~~~~~

This tutorial aims to complement the scaling capabilities of Occopus. With this solution users can scale their application without user intervention in a predefined scaling range to guarantee that its running always with the optimum level of resources. In this infrastructure, nodes are discovered by Consul, which is a service discovery tool also providing DNS service and are monitored by Prometheus, a monitoring software. Prometheus supports alert definitions which later will help you write custom scaling events. 

In this autoscaling example we implemented a multi-layered traditional load-balancing schema. On the upper layer, there are load balancer nodes organised into a cluster and prepared for scaling. The load balancer cluster is handling the load generated by secured http transfer (https) between the client and the underlying application. The application is also organised inside a scalable cluster to distribute the load generated by serving the client requests. For demonstrating this architecture, the application has been represented by the Data Avenue service, which implements data transfer between the client and a remote storage using various protocols (http, sftp, s3, ...). For further details about the software, please visit `the Data Avenue website <https://data-avenue.eu>`_ . Finally, in the lowest layer there is a Database node required by the instances of Data Avenue to store and retrieve infromation (authentication, statistics) for their operation.

In case, this architecture fits to your need, you may replace the Data Avenue (with its Database node) and integrate your own application. As a result, you will have a multi-level load-balancing infrastructure, where both load balancer nodes and application servers are dynamically scaled up and down depending on the load the corresponding cluster has.

**Features**

 - using Prometheus to monitor nodes and create user-defined scaling events
 - using load balancers to share system load between data nodes
 - using Consul as a DNS service discovery agent
 - using data nodes running the application

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, OCCI, Nova, etc.)
 - target cloud contains a base 14.04 ubuntu OS image with cloud-init support (image id, instance type)
 - start Occopus in Rest-API mode (# occopus-rest-service -h [Occopus ip address])

**Download**

You can download the example as `tutorial.examples.autoscaling-dataavenue <../../examples/autoscaling-dataavenue.tgz>`_ .

.. note::

   In this tutorial, we will use ec2 cloud resources (based on our ec2 tutorials in the basic tutorial section). However, feel free to use any Occopus-compatible cloud resource for the nodes - you can even use different types of resources for each node.

**Steps**

#. Edit ``nodes/node_definitions.yaml``. Configure the ``resource`` section as seen in the basic tutorials. For example, if you are using an ``ec2`` cloud, you have to set the following:

   - ``endpoint`` is an url of an EC2 interface of a cloud (e.g. `https://ec2.eu-west-1.amazonaws.com`).
   - ``regionname`` is the region name within an EC2 cloud (e.g. `eu-west-1`).
   - ``image_id`` is the image id (e.g. `ami-12345678`) on your EC2 cloud. Select an image containing a base os installation with cloud-init support!
   - ``instance_type`` is the instance type (e.g. `m1.small`) of your VM to be instantiated.
   - ``key_name``  optionally specifies the keypair (e.g. `my_ssh_keypair`) to be deployed on your VM.
   - ``security_group`` optionally specifies security settings (you can define multiple security groups in the form of a list, e.g. `sg-93d46bf7`) of your VM.
   - ``subnet_id`` optionally specifies subnet identifier (e.g. `subnet-644e1e13`) to be attached to the VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:da':
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
             ...
  

#. Optionally, edit the ``infra_as_dataavenue.yaml`` infrastructure descriptor file. Set the following attributes:

   - ``scaling`` is the interval in which the number of nodes can change (min,max). You can change da and lb nodes or leave them as they are.
   
   .. code::
      
      - &DA_cluster # Node Running your application
  	   name: da
	   type: da
  	   scaling:
 	     min: 1
 	     max: 10

   .. important::

      Keep in mind that Occopus has to start at least one node from each node type to work properly!

#. Optionally, you can edit the ``nodes/cloud_init_da.yaml`` node descriptor file. If you wish, you can replace the actually implemented Grid Data Avenue webapplication with your own one. Be careful, when modifying this example! 

   This autoscaling project scales the infrastructure over your application while you can run any application on it. You have to put your application code into the cloud_init_da.yaml file and make sure it starts automatically when the node boots up. This way every data node will run your application and load balancers will share the load between them. This solution fits to web applications serving high number of incoming http requests.

   .. note::

     For detailed explanation on cloud-init and its usage, please read `the cloud-init documentation <http://cloudinit.readthedocs.org/en/latest/topics/examples.html>`_!

#. Optionally, edit the ``nodes/cloud_init_prometheus.yaml`` node descriptor file's "Prometheus rules" section in case you want to implement new scaling rules. The actually implemented rules are working well and can be seen below.
   
	- ``{infra_id}`` is a built in Occopus variable and every alert has to implement it in their Labels!
	- ``node`` should be set to da or lb depending on which type of node the alerts should work.

   .. code::
      
       lb_cpu_utilization = 100 - (avg (rate(node_cpu{group="lb_cluster",mode="idle"}[60s])) * 100)
       da_cpu_utilization = 100 - (avg (rate(node_cpu{group="da_cluster",mode="idle"}[60s])) * 100)
 
    ALERT da_overloaded
      IF da_cpu_utilization > 50 
      FOR 1m
      LABELS {alert="overloaded", cluster="da_cluster", node="da", infra_id="{{infra_id}}"}
      ANNOTATIONS {
      summary = "DA cluster overloaded",
      description = "DA cluster average CPU/RAM/HDD utilization is overloaded"}
    ALERT da_underloaded
      IF da_cpu_utilization < 20
      FOR 2m
      LABELS {alert="underloaded", cluster="da_cluster", node="da", infra_id="{{infra_id}}"}
      ANNOTATIONS {
      summary = "DA cluster underloaded",
      description = "DA cluster average CPU/RAM/HDD utilization is underloaded"}
 		

   .. important::

      Autoscaling events (scale up, scale down) are based on Prometheus rules which act as thresholds, let’s say scale up if cpu usage > 80%. In this example you can see the implementation of a cpu utilization in your da-lb cluster with some threshold values. Please, always use infra_id in you alerts as you can see below since Occopus will resolve this variable to your actual infrastructure id. If you are planning to write new alerts after you deployed your infrastructure, you can copy the same infrastructure id to the new one. Also make sure that the "node" property is set in the Labels subsection, too. For more information about Prometheus rules and alerts, please visit: https://prometheus.io/docs/alerting/rules/


#. Edit the "variables" section of the ``infra_as_dataavenue.yaml`` file. Set the following attributes:

   - ``occopus_restservice_ip`` is the ip address of the host where you will start the occopus-rest-service
   - ``occopus_restservice_port`` is the port you will bind the occopus-rest-service to
   
   .. code::
 
    occopus_restservice_ip: "127.0.0.1"
    occopus_restservice_port: "5000" 

#. Make sure your authentication information is set correctly in your authentication file. You must set your authentication data for the ``resource`` you would like to use. Setting authentication information is described :ref:`here <authentication>`.

#. Load the node definitions into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start Occopus in REST service mode:

   .. code::

      occopus-rest-service --host [ip address to bind the service to]

#. Start deploying the infrastructure through the Occopus service: 

   .. code::

      curl -X POST http://[Occopus ip address]:5000/infrastructures/ --data-binary @infra_da.yaml

#. To test the down-scaling mechanism scale up manually the da nodes through the occopus REST interface and after a few minutes you can observe that the newly connected nodes will be automatically removed because the underloaded alert is firing. You can also check the status of your alerts during the testing at ``[PrometheusIP]:9090/alerts``.

   .. code::

      curl -X POST http://[Occopus ip address]:5000/infrastructures/[infrastructure_id]/scaleup/da
   
   .. important::

      Depending on the cloud you are using for you virtual machines it can take a few minutes to start a new node and connect it to your infrastructure. The connected nodes are present on prometheus's Targets page.

#. To test the up-scaling mechanism put some load on the data nodes with the command below. Just select one of your LB node and generate load on it with running the command below in a few copy. After a few minutes the cluster will be overloaded, the overloaded alerts will fire in Prometheus and a new da node will be started and connected to your cluster. Also, if you stop sending files for a while, the overloaded alerts will fire in Prometheus and one (or more) of the da nodes will be shut (scaled) down.

   To query the nodes and their ip addresses, use this command:

   .. code::

      curl -X GET http://[Occopus ip]:5000/infrastructures/[infrastructure_id]
   
   Once, you have the ip of the selected LB node, generate load on it by transferring a 1GB file using the command below. Do not forget to update the placeholder!

   .. code::

      curl -k -o /dev/null -H "X-Key: 1a7e159a-ffd8-49c8-8b40-549870c70e73" -H "X-URI:https://autoscale.s3.lpds.sztaki.hu/files_for_autoscale/1GB.dat" http://[LB node ip address]/blacktop3/rest/file 

   To check the status of alerts under Prometheus during the testing, keep watching the following url in your browser:

   .. code::
 
      http://[prometheus node ip]:9090/alerts
 
   .. important::

      Depending on the cloud you are using for you virtual machines it can take a few minutes to start a new node and connect it to your infrastructure. The connected nodes are present on prometheus's Targets page.

#. Finally, you may destroy the infrastructure using the infrastructure id.

   .. code::

      curl -X DELETE http://[occopus ip address]:5000/infrastructures/[infra id]


Hadoop-Cluster
~~~~~~~~~~~~~~
This tutorial sets up a complete Apache Hadoop infrastructure. It contains a Hadoop Master node and Hadoop Slave worker nodes, which can be scaled up or down. To register Hadoop Slave nodes Consul is used.

**Features**

 - creating two types of nodes through contextualisation
 - utilising health check against a predefined port
 - using scaling parameters to limit the number of Hadoop Slave nodes
 - manage cluster nodes with Consul

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g EC2, Nova, OCCI, etc.)
 - target cloud contains a base 14.04 Ubuntu OS image with cloud-init support
 - generated ssh key-pair (or for testing purposes one is attached)

**Download**

You can download the example as `tutorial.examples.hadoop-cluster <../../examples/hadoop-cluster.tgz>`_ .

.. note::

   In this tutorial, we will use nova cloud resources (based on our nova tutorials in the basic tutorial section). However, feel free to use any Occopus-compatible cloud resource for the nodes, but we suggest to instantiate all nodes in the same cloud.

**Steps**


#. Edit ``nodes/node_definitions.yaml``. For hadoop_master_node and for hadoop_slave_node nodes set the followings in their resource section as seen in the basic tutorials. For example, if you are using a ``nova`` cloud, you have to set the following:

   - ``endpoint`` must point to the endpoint (url) of your target Nova cloud.
   - ``project_id`` is the id of project you would like to use on your target Nova cloud.
   - ``user_domain_name`` is the user domain name you would like to use on your target Nova cloud.
   - ``image_id`` is the image id on your Nova cloud. Select an image containing a base os installation with cloud-init support!
   - ``flavor_name`` is the name of flavor to be instantiated on your Nova cloud.
   - ``key_name`` optionally sets the name of the keypair to be associated to the instance. Keypair name must be defined on the target nova cloud before launching the VM.
   - ``security_groups`` optionally specifies security settings (you can define multiple security groups in the form of a list) for your VM.
   - ``floating_ip`` optionally allocates new floating IP address to the VM if set to any value.
   - ``floating_ip_pool`` optionally specifies the name of pool from which the floating ip must be selected.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:hadoop_master_node':
         -
             resource:
                 type: nova
                 endpoint: replace_with_endpoint_of_nova_interface_of_your_cloud
                 project_id: replace_with_projectid_to_use
                 user_domain_name: Default
                 image_id: replace_with_id_of_your_image_on_your_target_cloud
                 network_id: replace_with_id_of_network_on_your_target_cloud
                 flavor_name: replace_with_id_of_the_flavor_on_your_target_cloud
                 key_name: replace_with_name_of_keypair_or_remove
                 security_groups:
                     -
                         replace_with_security_group_to_add_or_remove_section
                 floating_ip: add_yes_if_you_need_floating_ip_or_remove
                 floating_ip_pool: replace_with_name_of_floating_ip_pool_or_remove
            ...
     'node_def:hadoop_slave_node':
         -
             resource:
                 type: nova
                 endpoint: replace_with_endpoint_of_nova_interface_of_your_cloud
                 project_id: replace_with_projectid_to_use
                 user_domain_name: Default
                 image_id: replace_with_id_of_your_image_on_your_target_cloud
                 network_id: replace_with_id_of_network_on_your_target_cloud
                 flavor_name: replace_with_id_of_the_flavor_on_your_target_cloud
                 key_name: replace_with_name_of_keypair_or_remove
                 security_groups:
                     -
                         replace_with_security_group_to_add_or_remove_section
                 floating_ip: add_yes_if_you_need_floating_ip_or_remove
                 floating_ip_pool: replace_with_name_of_floating_ip_pool_or_remove
             ...

   .. important::

     Do not modify the values of the contextualisation and the health_check section’s attributes!
 
   .. important::

     Do not specify the server_name attribute for slaves so they are named automatically by Occopus to make sure node names are unique!
 
   .. note::

     If you want Occopus to monitor (health_check) your Hadoop Master and it is to be deployed in a different network, make sure you assign public (floating) IP to the Master node.

#. Components in the infrastructure connect to each other, therefore several port ranges must be opened for the VMs executing the components. Clouds implement port opening various way (e.g. security groups for OpenStack, etc). Make sure you implement port opening in your cloud for the following port ranges:

   .. code::

      TCP 22
      TCP 8025
      TCP 8042
      TCP 8088
      TCP 8300-8600
      TCP 9000
      TCP 50000-51000
 
#. Make sure your authentication information is set correctly in your authentication file. You must set your authentication data for the ``resource`` you would like to use. Setting authentication information is described :ref:`here <authentication>`.

#. Update the number of Hadoop Slave worker nodes if necessary. For this, edit the ``infra-occopus-hadoop.yaml`` file and modifiy the min and max parameter under the scaling keyword. Scaling is the interval in which the number of nodes can change (min, max). Currently, the minimum is set to 2 (which will be the initial number at startup), and the maximum is set to 10.

   .. code::

     - &S
    	name: hadoop_slave
    	type: hadoop_slave_node
    	scaling:
        	min: 2
        	max: 10
 
   .. important::

     Important: Keep in mind that Occopus has to start at least one node from each node type to work properly and scaling can be applied only for Hadoop Slave nodes in this example!

#. Load the node definitions into the database. Make sure the proper virtualenv is activated!

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure.

   .. code::

      occopus-build infra-hadoop-cluster.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

      List of nodes/ip addresses:
      hadoop_master:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      hadoop_slave:
          192.168.xxx.xxx (23f13bd1-25e7-30a1-c1b4-39c3da15a456)
          192.168.xxx.xxx (7b387348-b3a3-5556-83c3-26c43d498f39)

      14032858-d628-40a2-b611-71381bd463fa

#. You can check the  health and statistics of the cluster through the following web pages:

   .. code::
      
      Health of nodes: "http://<HadoopMasterIP>:50070"
      Job statistics: "http://<HadoopMasterIP>:8088"

#. To launch a Hadoop MapReduce job copy your input and executable files to the Hadoop Master node, and perform the submission described `here <https://hadoop.apache.org/docs/stable/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html>`_ . To access Hadoop Master node use the keypair defined in the descriptors. 

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

