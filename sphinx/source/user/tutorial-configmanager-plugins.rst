.. _tutorial-configmanager-plugins:

Tutorials on config manager plugins
===================================

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

