.. _tutorial:

Tutorial
========

In this section, examples will be shown, how Occopus can be used. Each subsection details an infrastructure by which the user can learn how the different features can be used, or how the different plugins or resources can be utilised.

Please, note that the following examples require a properly configured Occopus, therefore we suggest to continue this section if you already followed the instructions written in the :ref:`Installation <installation>` section.

EC2-Helloworld
--------------
This tutorial sets up an infrastructure containing a single node. The node will receive information (i.e. a message string) through contextualisation. The node will store this information in ``/tmp`` directory.

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

#. Edit ``nodes/node_definitions.yaml``. For ``ec2_helloworld_node`` set the followings in its ``resource`` section:

   - ``endpoint`` is an url of an EC2 interface of a cloud (e.g. `https://ec2.eu-west-1.amazonaws.com`). 
   - ``regionname`` is the region name within an EC2 cloud (e.g. `eu-west-1`).
   - ``image_id`` is the image id (e.g. `ami-12345678`) on your EC2 cloud. Select an image containing a base os installation with cloud-init support!
   - ``instance_type`` is the instance type (e.g. `m1.small`) of your VM to be instantiated.
   - ``key_name``  optionally specifies the keypair (e.g. `my_ssh_keypair`) to be deployed on your VM. 
   - ``security_group`` optionally specifies security settings (you can define multiple security groups in the form of a list, e.g. `sg-93d46bf7`) of you VM.
   - ``subnet_id`` optionally specifies subnet identifier (e.g. `subnet-644e1e13`) to be attached to the VM. 

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

#. Make sure your authentication information is set correctly in your authentication file. You must set your access key and secret key in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Import the node definition for ``ec2_helloworld_node`` node into the database. 

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

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
This tutorial sets up an infrastructure containing a single node. The node will receive information (i.e. a message string) through contextualisation. The node will store this information in ``/tmp`` directory.

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

#. Edit ``nodes/node_definitions.yaml``. For ``occi_helloworld_node`` set the followings in its ``resource`` section:

   - ``endpoint`` is an url of an Occi interface of a cloud (e.g. `https://carach5.ics.muni.cz:11443`) stored in the EGI AppDB. 
   - ``os_tpl`` is an image identifier for Occi (e.g. `os_tpl#uuid_egi_ubuntu_server_14_04_lts_fedcloud_warg_131`) stored in the EGI AppDB. Select an image containing a base os installation with cloud-init support!
   - ``resource_tpl`` is the instance type in Occi (e.g. `http://fedcloud.egi.eu/occi/compute/flavour/1.0#medium`) stored in the EGI AppDB.
   - ``link``  specifies the network (e.g. `https://carach5.ics.muni.cz:11443/network/24` and/or storage resources to be attached to the VM. 
   - ``public_key`` specifies the path to your ssh public key (e.g. `/home/user/.ssh/authorized_keys`) to be deployed on the target VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide. 

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
                 public_key: replace_with_path_to_your_ssh_public_key

#. Make sure your authentication information is set correctly in your authentication file. You must set the path of your VOMS proxy in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Import the node definition for ``occi_helloworld_node`` node into the database. 

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-occi-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

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

OCCI-Ping
---------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The sender node will store the outcome of ping in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:

 - creating two nodes with dependencies (i.e ordering of deployment)
 - querying a node's ip address and passing the address to another
 - using the occi resource handler

**Prerequisites**

 - accessing an OCCI cloud through its OCCI interface (endpoint, X.509 VOMS proxy)
 - target cloud contains a base OS image with cloud-init support (os_tpl, resource_tpl)
 - properly installed occi command-line client utility (occi command)

**Download**

You can download the example as `tutorial.examples.occi-ping <../../examples/occi-ping.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit ``nodes/node_definitions.yaml``. Both, for ``occi_ping_receiver_node`` and for ``occi_ping_sender_node`` set the followings in its ``resource`` section:
   
   - ``endpoint`` is an url of an Occi interface of a cloud (e.g. `https://carach5.ics.muni.cz:11443`) stored in the EGI AppDB. 
   - ``os_tpl`` is an image identifier for Occi (e.g. `os_tpl#uuid_egi_ubuntu_server_14_04_lts_fedcloud_warg_131`) stored in the EGI AppDB. Select an image containing a base os installation with cloud-init support!
   - ``resource_tpl`` is the instance type in Occi (e.g. `http://fedcloud.egi.eu/occi/compute/flavour/1.0#medium`) stored in the EGI AppDB.
   - ``link``  specifies the network (e.g. `https://carach5.ics.muni.cz:11443/network/24` and/or storage resources to be attached to the VM. 
   - ``public_key`` specifies the path to your ssh public key (e.g. `/home/user/.ssh/authorized_keys`) to be deployed on the target VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide. 

   .. code::

     'node_def:occi_ping_receiver_node':
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
     'node_def:occi_ping_sender_node':
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

#. Make sure your authentication information is set correctly in your authentication file. You must set the path of your VOMS proxy in the authentication file. Setting authentication information is described :ref:`here <authentication>`.


#. Load the node definition for ``occi_ping_receiver_node`` and ``occi_ping_sender_node`` nodes into the database.
   
   .. code::

      occopus-import nodes/node_definitions.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-occi-ping.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::
   
      List of ip addresses:
      ping_receiver:
          192.168.xxx.xxx (f639a4ad-e9cb-478d-8208-9700415b95a4)
      ping_sender:
          192.168.yyy.yyy (99bdeb76-2295-4be7-8f14-969ab9d222b8)

      30f566d1-9945-42be-b603-795d604b362f

#. Check the result on your virtual machine.

   .. code::

      ssh user@192.168.xxx.xxx
      # cat /tmp/message.txt
      Hello World! I am the receiver node created by Occopus.
      # cat /tmp/ping-result.txt
      PING 192.168.xxx.xxx (192.168.xxx.xxx) 56(84) bytes of data.
      64 bytes from 192.168.xxx.xxx: icmp_seq=1 ttl=64 time=2.74 ms
      64 bytes from 192.168.xxx.xxx: icmp_seq=2 ttl=64 time=0.793 ms
      64 bytes from 192.168.xxx.xxx: icmp_seq=3 ttl=64 time=0.865 ms
      64 bytes from 192.168.xxx.xxx: icmp_seq=4 ttl=64 time=0.882 ms
      64 bytes from 192.168.xxx.xxx: icmp_seq=5 ttl=64 time=0.786 ms

      --- 192.168.xxx.xxx ping statistics ---
      5 packets transmitted, 5 received, 0% packet loss, time 4003ms
      rtt min/avg/max/mdev = 0.786/1.215/2.749/0.767 ms

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 30f566d1-9945-42be-b603-795d604b362f

