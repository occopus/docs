.. _tutorial:

Tutorial
========

In this section, examples will be shown, how Occopus can be used. Each subsection details an infrastructure by which the user can learn how the different features can be used, or how the different plugins or resources can be utilised.

Please, note that the following examples require a properly configured Occopus, therefore we suggest to continue this section if you already followed the instructions written in the :ref:`Installation <installation>` section.

EC2-Helloworld
--------------
This tutorial sets up an infrastructure containing a single node. The node will receive information (i.e. a message string) through contextualisation. The node will store this information in ``/tmp/helloworld`` file.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node
 - using the ec2 resource handler

**Prerequisites**

 - accessing a cloud through EC2 interface (access key, secret key, endpoint, regionname)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

**Download**

You can download the example as `tutorial.examples.ec2-helloworld <../../examples/ec2-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit ``nodes/node_definitions.yaml``. In the *resource* section of the node called ``ec2_helloworld_node``, first set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud. Next, set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``). Select an image containing a base os installation with cloud-init support. Optionally (in case of Amazon AWS and OpenStack EC2), you should also set the keypair (e.g. ``my_ssh_keypair``), the security groups (you can define multiple security groups in the form of a list, e.g. ``sg-93d46bf7``) and the subnet identifier (e.g. ``subnet-644e1e13``) to be attached to the VM. 

For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide. 

   .. code::

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

#. Make sure your authentication information is set correclty in your authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Import the node definition for ``ec2_helloworld_node`` node into the database. 

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain -l** command.

   .. code::

      List of nodes/ip addresses:
      helloworld:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      14032858-d628-40a2-b611-71381bd463fa

#. Check the result on your virtual machine.

   .. code::
        
      ssh user@192.168.xxx.xxx
      # cat /tmp/helloworld.txt
      Hello World! I have been created by Occopus

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

OCCI-Helloworld
---------------
This tutorial sets up an infrastructure containing a single node. The node will receive information (i.e. a message string) through contextualisation. The node will store this information in ``/tmp/helloworld`` file.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node
 - using the occi resource handler

**Prerequisites**

 - accessing an OCCI cloud through its OCCI interface (endpoint, X.509 VOMS proxy)
 - target cloud contains a base OS image with cloud-init support (os_tpl, resource_tpl)
 - properly installed occi command-line client utility (occi command)

**Download**

You can download the example as `tutorial.examples.occi-helloworld <../../examples/occi-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit ``nodes/node_definitions.yaml``. In the *resource* section of the node called ``occi_helloworld_node``, first set the ``endpoint`` (e.g. ``https://carach5.ics.muni.cz:11443``) of Occi interface to your target cloud. You can get the proper url from the EGI AppDB. Next, set the os_tpl (e.g. ``os_tpl#uuid_egi_ubuntu_server_14_04_lts_fedcloud_warg_131``) and resource_tpl (e.g. ``http://fedcloud.egi.eu/occi/compute/flavour/1.0#medium``) which can also be retrieved from EGI AppDB. The ``link`` keyword specifies the network (e.g. ``https://carach5.ics.muni.cz:11443/network/24`` and/or storage resources to be attached to the VM. Select an image containing a base os installation with cloud-init support. For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide. 

   .. code::

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

#. Make sure your authentication information is set correclty in your authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Import the node definition for ``occi_helloworld_node`` node into the database. 

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-occi-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain -l** command.

   .. code::

      List of nodes/ip addresses:
      helloworld:
          192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
      14032858-d628-40a2-b611-71381bd463fa

#. Check the result on your virtual machine.

   .. code::
        
      ssh user@192.168.xxx.xxx
      # cat /tmp/helloworld.txt
      Hello World! I have been created by Occopus

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 14032858-d628-40a2-b611-71381bd463fa

