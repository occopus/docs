.. _tutorial-configmanager-plugins:

Config manager plugins
======================

In this section more advanced solutions will be shown. The examples will introduce complex infrastructures or will introduce more complex features of the Occopus tool.

Please, note that the following examples require a properly configured Occopus, therefore we suggest to continue this section if you already followed the instructions written in the :ref:`Installation <installation>` section.

Chef-Apache2
~~~~~~~~~~~~
This tutorial uses Chef as a configuration management tool to deploy a one-node infrastructure containing an Apache2 web server.

**Features**

 - using Chef as a configuration management tool to deploy services
 - assembling the run-lists of the chef-clients on the nodes

**Prerequisites**

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, Azure, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - accessing the Chef server as user by Occopus (user name, user key)
 - accessing the Chef server as client by the nodes (validator client name, validator client key)
 - ``apache2`` community recipe (available at Chef Supermarket) and its dependencies uploaded to target Chef Server

**Download**

You can download the example as `tutorial.examples.chef-apache2 <https://raw.githubusercontent.com/occopus/docs/master/tutorials/chef-apache2.tar.gz>`_ .

**Steps**

#. Open the file ``nodes/node_definitions.yaml`` and edit the resource section of the nodes labelled by ``node_def:``.

   - you must select an :ref:`Occopus compatible resource plugin <user-doc-clouds>`
   - you can find and specify the relevant :ref:`list of attributes for the plugin <userdefinitionresourcesection>`
   - you may follow the help on :ref:`collecting the values of the attributes for the plugin <user-doc-collecting-resources>`
   - you may find a resource template for the plugin in the :ref:`resource plugin tutorials <tutorial-resource-plugins>`

   The downloadable package for this example contains a resource template for the EC2 plugin.

#. Make sure your authentication information is set correctly in your authentication file. You must set your email and password in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Edit ``nodes/node_definitions.yaml``. Configure the ``config_management``. Set the ``endpoint`` to the url of your Chef Server.

   .. code:: yaml

     'node_def:chef_apache2_node':
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

   .. code:: yaml

      Example:

      validation_name: "yourorg-validator"
      validation_key: |
          -----BEGIN RSA PRIVATE KEY-----
          YOUR-ORGS-VALIDATION-KEY-HERE
          -----END RSA PRIVATE KEY-----

   .. important::

      Make sure you do not mix the ``validator client`` with ``user`` belonging to the Chef Server.

   .. code:: yaml

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

   .. code:: bash

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code:: bash

      occopus-build infra-chef-apache2.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code:: bash

      List of nodes/ip addresses:
      apache2:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code:: bash

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

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, Azure, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - accessing the Chef server as user by Occopus (user name, user key)
 - accessing the Chef server as client by the nodes (validator client name, validator client key)
 - ``wordpress`` community recipe (available at Chef Supermarket) and its dependencies uploaded to target Chef Server
 - ``database-setup`` recipe (provided in example package at Download) uploaded to target Chef server

**Download**

You can download the example as `tutorial.examples.chef-wordpress <https://raw.githubusercontent.com/occopus/docs/master/tutorials/chef-wordpress.tar.gz>`_ .

**Steps**

#. Open the file ``nodes/node_definitions.yaml`` and edit the resource section of the nodes labelled by ``node_def:``.

   - you must select an :ref:`Occopus compatible resource plugin <user-doc-clouds>`
   - you can find and specify the relevant :ref:`list of attributes for the plugin <userdefinitionresourcesection>`
   - you may follow the help on :ref:`collecting the values of the attributes for the plugin <user-doc-collecting-resources>`
   - you may find a resource template for the plugin in the :ref:`resource plugin tutorials <tutorial-resource-plugins>`

   The downloadable package for this example contains a resource template for the EC2 plugin.

#. Edit ``nodes/node_definitions.yaml``. For each node, configure the ``config_management``. Set the ``endpoint`` to the url of your Chef Server.

   .. code:: yaml

     'node_def:chef_mysql_node':
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
     'node_def:chef_wordpress_node':
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

   .. code:: yaml

      Example:

      validation_name: "yourorg-validator"
      validation_key: |
          -----BEGIN RSA PRIVATE KEY-----
          YOUR-ORGS-VALIDATION-KEY-HERE
          -----END RSA PRIVATE KEY-----

   .. important::

      Make sure you do not mix the ``validator client`` with ``user`` belonging to the Chef Server.

   .. code:: yaml

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

   .. code:: yaml

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

   .. code:: bash

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code:: bash

      occopus-build infra-chef-wordpress.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code:: bash

      List of nodes/ip addresses:
      mysql-server:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      wordpress:
          192.168.xxx.xxx (894fe127-28c9-4c8f-8c5f-2f120c69b9c3)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code:: bash

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

 - accessing a cloud through an Occopus-compatible interface (e.g. EC2, Azure, Nova, etc.)
 - target cloud contains a base OS image with cloud-init support (image id, instance type)
 - ``wordpress-init`` puppet recipe (provided in example package at Download)
 - ``mysql-init`` puppet recipe (provided in example package at Download)

**Download**

You can download the example as `tutorial.examples.puppet-solo-wordpress <https://raw.githubusercontent.com/occopus/docs/master/tutorials/puppet-solo-wordpress.tar.gz>`_ .

**Steps**

#. Open the file ``nodes/node_definitions.yaml`` and edit the resource section of the nodes labelled by ``node_def:``.

   - you must select an :ref:`Occopus compatible resource plugin <user-doc-clouds>`
   - you can find and specify the relevant :ref:`list of attributes for the plugin <userdefinitionresourcesection>`
   - you may follow the help on :ref:`collecting the values of the attributes for the plugin <user-doc-collecting-resources>`
   - you may find a resource template for the plugin in the :ref:`resource plugin tutorials <tutorial-resource-plugins>`

   The downloadable package for this example contains a resource template for the EC2 plugin.

#. Edit ``infra-puppet-solo-wordpress.yaml``. Set your desired root password, database name, username, and user password for your MySQL database in the variables section. These parameters will be applied when creating the mysql database and also used by wordpress node when connecting to mysql.

   .. code:: yaml

     ...
     variables:
        mysql_root_password: replace_with_database_root_password
        mysql_database_name: replace_with_database_name
        mysql_dbuser_username: replace_with_database_username
        mysql_dbuser_password: replace_with_database_user_password

#. Load the node definitions into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition or any imported (e.g. contextualisation) file changes!

   .. code:: bash

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code:: bash

      occopus-build infra-puppet-solo-wordpress.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code:: bash

      List of nodes/ip addresses:
      mysql-server:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      wordpress:
          192.168.xxx.xxx (894fe127-28c9-4c8f-8c5f-2f120c69b9c3)
      14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code:: bash

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

