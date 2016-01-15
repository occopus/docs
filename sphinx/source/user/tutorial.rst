.. _tutorial:

Tutorial
========

In this section, examples will be shown, how this tool can be used. Each
subsection details a certain infrastructure by which the user can learn how the
different features can be utilised, or how the different plugins or clouds can
be driven.

Please, note that the following examples require a properly configured tool,
therefore we suggest to start with the :ref:`Installation <installation>` section.

EC2-Helloworld
--------------
This tutorial sets up an infrastructure containing a single node. The node will
receive information (i.e. a message string) through contextualisation. The node
will store this information in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

**Prerequisites**

 - accessing a cloud through EC2 interface (access key, secret key, endpoint, regionname)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

**Download**

You can download the example as `tutorial.examples.ec2-helloworld <../../examples/ec2-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
    .. code::

        my_ec2_cloud:
            protocol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key. 
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for the node called ``hw_node``. Select an image containing a base os installation with cloud-init support. Optionally (in case of Amazon AWS and OpenStack EC2), you should also set the keypair (e.g. ``my_ssh_keypair``), the security groups (you can define multiple security groups in the form of a list, e.g. ``sg-93d46bf7``) and the subnet identifier (e.g. ``subnet-644e1e13``) to be attached to the VM.
     .. code::

        ... 
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

#. Load the node definition for ``helloworld`` node into the database. 
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        helloworld:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. Check the result on your virtual machine.
    .. code::
        
        ssh user@192.168.xxx.xxx
        # cat /tmp/helloworld.txt
        Hello World! I have been created by OCCO

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 14032858-d628-40a2-b611-71381bd463fa

EC2-Ping
--------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The node will store the outcome of ping in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

**Prerequisites**

 - accessing a cloud through EC2 interface (access key, secret key, endpoint, regionname)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

**Download**

You can download the example as `tutorial.examples.ec2-ping <../../examples/ec2-ping.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
    .. code::

        my_ec2_cloud:
            protocol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key. 
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for the nodes called ``ping_receiver_node`` and ``ping_sender_node``. Select an image containing a base os installation with cloud-init support. Optionally (in case of Amazon AWS and OpenStack EC2), you should also set the keypair (e.g. ``my_ssh_keypair``), the security groups (you can define multiple security groups in the form of a list, e.g. ``sg-93d46bf7``) and the subnet identifier (e.g. ``subnet-644e1e13``) to be attached to the VM. Do not forget to set the attributes for both nodes!
     .. code::

        'node_def:ping_receiver_node':
            ... 
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
        'node_def:ping_sender_node':
            ...
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

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database. 
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-ping.yaml 

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
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
        Hello World! I am the sender node.
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


#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 30f566d1-9945-42be-b603-795d604b362f


Nova-Helloworld
---------------
This tutorial sets up an infrastructure containing a single node. The node will
receive information (i.e. a message string) through contextualisation. The node
will store this information in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

**Prerequisites**

 - accessing an OpenStack cloud through Nova interface (access key, secret key, endpoint, tenant name)
 - target cloud contains a base OS image with cloud-init support (image id, flavor)

**Download**

You can download the example as `tutorial.examples.nova-helloworld <../../examples/nova-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``tenant_name`` of your Nova interface to your target cloud.
    .. code::

        my_nova_cloud:
            protocol: nova
            name: MYCLOUD
            target:
                auth_url: replace_with_endpoint_of_nova_interface_of_your_cloud
                tenant_name: replace_with_tenant_to_use

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` and  ``password`` to match your Nova login credentials.
     .. code::

        username: replace_with_your_nova_username
        password: replace_with_your_nova_password

#. Edit ``init_data/uds_init_data.yaml``. Set the image id, flavor id, keypair name, any security groups and floating IP for the node called ``hw_node``. Select an image containing a base os installation with cloud-init support.
     .. code::

        ... 
        image_id: replace_with_id_of_your_image_on_your_target_cloud
        flavor_name: replace_with_id_of_the_flavor_on_your_target_cloud
        key_name: replace_with_name_of_keypair_to_be_used
        security_groups:
            -
                replace_with_security_group_to_add
            -
                replace_with_security_group_to_add
        floating_ip: add_yes_if_you_need_floating_ip
        ...

#. Load the node definition for ``helloworld`` node into the database. 
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-helloworld.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        helloworld:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. Check the result on your virtual machine.
    .. code::
        
        ssh user@192.168.xxx.xxx
        # cat /tmp/helloworld.txt
        Hello World! I have been created by OCCO

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 14032858-d628-40a2-b611-71381bd463fa


Nova-Ping
---------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The node will store the outcome of ping in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

**Prerequisites**

 - accessing an OpenStack cloud through Nova interface (access key, secret key, endpoint, tenant name)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

**Download**

You can download the example as `tutorial.examples.nova-ping <../../examples/nova-ping.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``tenant_name`` of your Nova interface to your target cloud.
    .. code::

        my_nova_cloud:
            protocol: nova
            name: MYCLOUD
            target:
                auth_url: replace_with_endpoint_of_nova_interface_of_your_cloud
                tenant_name: replace_with_tenant_to_use

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` and  ``password`` to match your Nova login credentials.
     .. code::

        username: replace_with_your_nova_username
        password: replace_with_your_nova_password

#. Edit ``init_data/uds_init_data.yaml``. Set the image id, flavor id, keypair name, any security groups and floating IP for the nodes called ``ping_receiver_node`` and ``ping_sender_node``. Select an image containing a base os installation with cloud-init support.
     .. code::

        'node_def:ping_receiver_node':
            ... 
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            flavor_name: replace_with_id_of_the_flavor_on_your_target_cloud
            key_name: replace_with_name_of_keypair_to_be_used
            security_groups:
                -
                    replace_with_security_group_to_add
                -
                    replace_with_security_group_to_add
            floating_ip: add_yes_if_you_need_floating_ip
            ...
        'node_def:ping_sender_node':
            ...
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            flavor_name: replace_with_id_of_the_flavor_on_your_target_cloud
            key_name: replace_with_name_of_keypair_to_be_used
            security_groups:
                -
                    replace_with_security_group_to_add
                -
                    replace_with_security_group_to_add
            floating_ip: add_yes_if_you_need_floating_ip
            ...

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database. 
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-ping.yaml 

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
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
        Hello World! I am the sender node.
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


#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 30f566d1-9945-42be-b603-795d604b362f


OCCI-Helloworld
---------------
This tutorial sets up an infrastructure containing a single node. The node will
receive information (i.e. a message string) through contextualisation. The node
will store this information in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

**Prerequisites**

 - accessing an OCCI cloud through its OCCI interface (endpoint, X.509 VOMS proxy)
 - target cloud contains a base OS image with cloud-init support (os_tpl, resource_tpl)

**Download**

You can download the example as `tutorial.examples.occi-helloworld <../../examples/occi-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` to the OCCI service URL of your target cloud, and set ``auth_data`` to the path of your X.509 VOMS proxy certificate accepted by the OCCI endpoint for authentication.
    .. code::

        my_occi_cloud:
            protocol: occi
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_occi_interface_of_your_cloud
            auth_data: path_to_your_vomsified_x509_proxy

#. Edit ``init_data/uds_init_data.yaml``. Set the ``os_tpl``, ``resource_tpl``, and ``link`` (as needed) for the node called ``hw_node``. The variable ``os_tpl`` specifies the VM image to be used, ``resource_tpl`` selects the intance type to be used, and the optional list specified in ``link`` specifies the network and storage resources to be attached to the VM. Select an image containing a base os installation with cloud-init support.
     .. code::

        ...
        os_tpl: replace_with_id_of_your_image_on_your_target_cloud
        resource_tpl: replace_with_id_of_the_resource_on_your_target_cloud
        link:
            -
                replace_with_link_to_attach
            -
                replace_with_link_to_attach
        ...

#. Load the node definition for ``helloworld`` node into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-helloworld.yaml

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        helloworld:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. Check the result on your virtual machine.
    .. code::

        ssh user@192.168.xxx.xxx
        # cat /tmp/helloworld.txt
        Hello World! I have been created by OCCO

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 14032858-d628-40a2-b611-71381bd463fa


OCCI-Ping
---------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The node will store the outcome of ping in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

**Prerequisites**

 - accessing an OCCI cloud through its OCCI interface (endpoint, X.509 VOMS proxy)
 - target cloud contains a base OS image with cloud-init support (os_tpl, resource_tpl)

**Download**

You can download the example as `tutorial.examples.occi-ping <../../examples/occi-ping.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` to the OCCI service URL of your target cloud, and set ``auth_data`` to the path of your X.509 VOMS proxy certificate accepted by the OCCI endpoint for authentication.
    .. code::

        my_occi_cloud:
            protocol: occi
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_occi_interface_of_your_cloud
            auth_data: path_to_your_vomsified_x509_proxy

#. Edit ``init_data/uds_init_data.yaml``. Set the ``os_tpl``, ``resource_tpl``, and ``link`` (as needed) for the nodes called ``ping_receiver_node`` and ``ping_sender_node``. The variable ``os_tpl`` specifies the VM image to be used, ``resource_tpl`` selects the intance type to be used, and the optional list specified in ``link`` specifies the network and storage resources to be attached to the VM. Select an image containing a base os installation with cloud-init support.
     .. code::

        'node_def:ping_receiver_node':
            ...
            os_tpl: replace_with_id_of_your_image_on_your_target_cloud
            resource_tpl: replace_with_id_of_the_resource_on_your_target_cloud
            link:
                -
                    replace_with_link_to_attach
                -
                    replace_with_link_to_attach
            ...
        'node_def:ping_sender_node':
            ...
            os_tpl: replace_with_id_of_your_image_on_your_target_cloud
            resource_tpl: replace_with_id_of_the_resource_on_your_target_cloud
            link:
                -
                    replace_with_link_to_attach
                -
                    replace_with_link_to_attach
            ...

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-ping.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
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
        Hello World! I am the sender node.
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


#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 30f566d1-9945-42be-b603-795d604b362f


CloudBroker-RunExe
------------------
This tutorial sets up an infrastructure containing one node with the help of the CloudBroker
Platform. The node initiated is using the a VM image which executes the input file uploaded
with the name ``execute.bin``.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - uploading the content of two files, one as the executable, and one as the input for the executable.

**Prerequisites**

 - accessing a CloudBroker Platform instance (URL, username and password)
 - Software, Executabe, Resource, Region and Instance type properly registered

**Download**

You can download the example as `tutorial.examples.cloudbroker-runexe <../../examples/cloudbroker-runexe.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``target`` to match the URL of the CloudBroker service you are accessing.
    .. code::

        cloudbroker:
            protocol: cloudbroker
            name: CloudBroker
            target: https://cloudsme-prototype.cloudbroker.com/

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``email`` and  ``password`` to match your CloudBroker login credentials.
     .. code::

        email: replace_with_your_cloudbroker_login
        password: replace_with_your_cloudbroker_password

#. Edit ``init_data/uds_init_data.yaml``. Set the ``software_id``, ``executable_id``, ``resource_id``, ``region_id``, and ``instance_type_id`` variables to match a software on a resource which is capable of running user-uploaded executables.
     .. code::

        ...
        attributes:
                software_id: 840ddb5e-9ecd-4e28-87ed-5f8f5a144f48
                executable_id: 1211d2e7-de65-4e57-b956-c5bf1d5a66af
                resource_id: 6df28843-8759-4270-8389-6cdc069bd8f2
                region_id: fc522ff3-039a-4f43-a810-1d10402dfd3a
                instance_type_id: 9ce671ff-eb7f-4bfc-b3bf-cefb6f6dafc2
        ...

#. Load the node definition for the node into the database. 
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-runexe.yaml 

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        Single:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 30f566d1-9945-42be-b603-795d604b362f


CloudBroker-Ping
----------------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The node will store the outcome of ping in ``/tmp`` directory.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

**Prerequisites**

 - accessing a CloudBroker Platform instance (URL, username and password)
 - Software, Executabe, Resource, Region and Instance type properly registered

**Download**

You can download the example as `tutorial.examples.cloudbroker-ping <../../examples/cloudbroker-ping.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``target`` to match the URL of the CloudBroker service you are accessing.
    .. code::

        cloudbroker:
            protocol: cloudbroker
            name: CloudBroker
            target: https://cloudsme-prototype.cloudbroker.com/

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``email`` and  ``password`` to match your CloudBroker login credentials.
     .. code::

        email: replace_with_your_cloudbroker_login
        password: replace_with_your_cloudbroker_password

#. Edit ``init_data/uds_init_data.yaml``. Set the ``software_id``, ``executable_id``, ``resource_id``, ``region_id``, and ``instance_type_id`` variables to match a software on a resource which is capable of running user-uploaded executables for the nodes called ``ping_receiver_node`` and ``ping_sender_node``.
     .. code::

        'node_def:ping_receiver_node':
            ...
        attributes:
                software_id: 840ddb5e-9ecd-4e28-87ed-5f8f5a144f48
                executable_id: 1211d2e7-de65-4e57-b956-c5bf1d5a66af
                resource_id: 6df28843-8759-4270-8389-6cdc069bd8f2
                region_id: fc522ff3-039a-4f43-a810-1d10402dfd3a
                instance_type_id: 9ce671ff-eb7f-4bfc-b3bf-cefb6f6dafc2
            ...
        'node_def:ping_sender_node':
            ...
        attributes:
                software_id: 840ddb5e-9ecd-4e28-87ed-5f8f5a144f48
                executable_id: 1211d2e7-de65-4e57-b956-c5bf1d5a66af
                resource_id: 6df28843-8759-4270-8389-6cdc069bd8f2
                region_id: fc522ff3-039a-4f43-a810-1d10402dfd3a
                instance_type_id: 9ce671ff-eb7f-4bfc-b3bf-cefb6f6dafc2
            ...

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-ping.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
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
        Hello World! I am the sender node.
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


#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 30f566d1-9945-42be-b603-795d604b362f

Chef - Apache2
--------------
This tutorial demonstrates the capabilites of Occopus to work together with chef, by setting up a single-node infrastructure with an Apache2 web server service on it.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - running a Chef recipe to configure the node

**Prerequisites**

 - chef server for your organization
 - chef-validator key for occopus
 - accessing a cloud through ec2 interface
 - target cloud contains a base OS image with cloud-init support
 - apache2 chef recipe (available via the community store) uploaded to chef server

**Download**

You can download the example as `tutorial.examples.chef-apache2 <../../examples/chef-apache2.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
     .. code::

        my_ec2_cloud:
            protcol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Also in ``conf/components.yaml``, provide the url and client name for your Chef server.
    .. code::

        servicecomposer: !ServiceCimposer &sc
            protocol: chef
            url: replace_with_url_of_chef_server
            key: !text_import
                url: file://client_key.pem
            client: replace_with_name_of_chef_client 


#. Create ``conf/client_key.pem`` and copy the private key of your chef client into it.

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key.
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/apache2_context.yaml``. Provide the url of your Chef server and the chef-validator key. This context file validates the occopus for the chef server. Please note that quotation marks around the url are necessary.
    .. code::

        chef:
            install_type: omnibus
            omnibus_url: "https://www.opscode.com/chef/install.sh"
            force_install: false
            server_url: "replace_with_your_chef_server_url"
            environment: {{infra_id}}
            node_name: {{node_id}}
            validation_name: "chef-validator"
            validation_key: |
                replace_with_chef-validator_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for the node called ``chef_apache2``. Select an image containing a base os installation with cloud-init support. Optionally (in case of Amazon AWS and OpenStack EC2), you should also set the keypair (e.g. ``my_ssh_keypair``), the security groups (you can define multiple security groups in the form of a list, e.g. ``sg-93d46bf7``) and the subnet identifier (e.g. ``subnet-644e1e13``) to be attached to the VM.
     .. code::

        ...
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

#. Load the node definition for ``chef_apache2`` node into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-chef-apache2.yaml

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        helloworld:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. You can check the result on your virtual machine.
    .. code::

        ssh user@192.168.xxx.xxx
        # apache2 -V

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 14032858-d628-40a2-b611-71381bd463fa

Chef - WPress+MySQL 
-------------------
This tutorial demonstrates the capabilites of Occopus to work together with chef and how certain variables can be passed around. For this, Occopus creates a wordpress node and a separate mysql database node. The wordpress node automatically receives the parameters of the database.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - using Chef to configure the nodes
 - providing the database node's parameters as chef variables to the wordpress node

**Prerequisites**

 - chef server for your organization
 - chef-validator key for occopus
 - accessing a cloud through ec2 interface
 - target cloud contains a base OS image with cloud-init support
 - the database-setup cookbook (included in the tutorial) and its prerequisite cookbooks (mysql, database) uploaded to your chef server
 - the wordpress cookbook (available via community store) and its prerequisite cookbooks uploaded to your chef server

**Download**

You can download the example as `tutorial.examples.chef-wordpress <../../examples/chef-wordpress.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Edit the infrastructure description, ``infra_chef_wordpress.yaml``. Set the database's desired name, the username and password, and the root password.
    .. code::
        
        variables:
            mysql_root_password: replace_with_database_root_password
            mysql_database_name: replace_with_database_name
            mysql_dbuser_username: replace_with_database_name
            mysql_dbuser_password: replace_with_database_user_password
    
#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
     .. code::

        my_ec2_cloud:
            protcol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Also in ``conf/components.yaml``, provide the url and client name for your Chef server.
    .. code::

        servicecomposer: !ServiceCimposer &sc
            protocol: chef
            url: replace_with_url_of_chef_server
            key: !text_import
                url: file://client_key.pem
            client: replace_with_name_of_chef_client 


#. Create ``conf/client_key.pem`` and copy the private key of your chef client into it.

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key.
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/wordpress_context.yaml``. Provide the url of your Chef server and the chef-validator key. This context file validates the occopus for the chef server. Please note that quotation marks around the url are necessary.
    .. code::

        chef:
            install_type: omnibus
            omnibus_url: "https://www.opscode.com/chef/install.sh"
            force_install: false
            server_url: "replace_with_your_chef_server_url"
            environment: {{infra_id}}
            node_name: {{node_id}}
            validation_name: "chef-validator"
            validation_key: |
                replace_with_chef-validator_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for both the nodes called ``mysql_server`` and ``wordpress``. Select an image containing a base os installation with cloud-init support. Optionally (in case of Amazon AWS and OpenStack EC2), you should also set the keypair (e.g. ``my_ssh_keypair``), the security groups (you can define multiple security groups in the form of a list, e.g. ``sg-93d46bf7``) and the subnet identifier (e.g. ``subnet-644e1e13``) to be attached to the VM.
     .. code::
        
       'node_def:mysql_server':
        ...
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
        'node-def:wordpress':
        ...
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

#. Load the node definition for ``chef_wordpress`` node into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml infra-chef-wordpress.yaml

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.
    .. code::

        List of ip addresses:
        chef-wordpress:
            192.168.xxx.xxx (3116eaf5-89e7-405f-ab94-9550ba1d0a7c)
        14032858-d628-40a2-b611-71381bd463fa

#. You can check the result on your virtual machine.
    .. code::

        ssh user@192.168.xxx.xxx

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 14032858-d628-40a2-b611-71381bd463fa

Docker-Helloworld
-----------------
This tutorial sets up an infrastructure containing a single node. The node will
receive information (i.e. a message string) through environment variable. The node
will store this information in ``/root/message.txt`` file.

**Features**

In this example, the following features will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

**Prerequisites**

 - Accessing a docker host or a swarm cluster
 - Note: encrypted connection is not supported yet

**Download**

You can download the example as `tutorial.examples.docker-helloworld <../../examples/docker-helloworld.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``base_url`` of your docker host or swarm cluster.
    .. code::

        cloud_cfgs:
            docker:
                protocol: docker
                name: Docker
                base_url: unix://var/run/docker.sock #or tcp://$IP:$PORT

#. Load the node definition for ``docker-node`` into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml docker-helloworld.yaml

#. After successful finish, the node with ``ip address`` and ``node id`` is listed at the end of the logging messages and the identifier of the created infrastructure is returned. 

#. Check the result on your docker host.
    .. code::

        # docker ps
        CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS               NAMES
        13bb8c94b5f4        busybox_helloworld:latest   "sh -c /root/start.sh"   3 seconds ago       Up 2 seconds                            admiring_joliot

        # docker exec -it 13bb8c94b5f4 cat /root/message.txt
        Hello World! I have been created by OCCO.

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 6b19b640-1b41-4970-ab0a-b13a0c6e2800

Docker-Ping
-----------
This tutorial sets up an infrastructure containing two nodes. The ping-sender node will
ping the ping-receiver node. The node will store the outcome of ping in ``/root/ping-result.txt`` file.

**Features**

In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

**Prerequisites**

 - Accessing a docker host or a swarm cluster
 - In case of swarm cluster, multi-host (overlay) network must be available
 - Note: encrypted connection is not supported yet

**Download**

You can download the example as `tutorial.examples.docker-ping <../../examples/docker-ping.tgz>`_ .

**Steps**

The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``base_url`` of your docker host or swarm cluster.
    .. code::

        cloud_cfgs:
            docker:
                protocol: docker
                name: Docker
                base_url: unix://var/run/docker.sock #or tcp://$IP:$PORT

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database.
    .. code::

        occo-import-node init_data/redis_data.yaml

#. Start deploying the infrastructure. Make sure the proper virtualenv is activated.
    .. code::

       occo-infra-start --listips --cfg conf/occo.yaml docker-ping.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the created infrastructure is returned. Do not forget to store the identifier of the infrastructure to perform further operations on your infra.

#. Check the result on your docker container.
    .. code::

        # docker ps
        CONTAINER ID        IMAGE                       COMMAND                  CREATED             STATUS              PORTS               NAMES
        4e83c45e8378        busybox_ping:latest         "sh -c /root/start.sh"   16 seconds ago      Up 15 seconds                           romantic_brown
        10b27bc4d978        busybox_helloworld:latest   "sh -c /root/start.sh"   17 seconds ago      Up 16 seconds                           jovial_mayer

        # docker exec -it 4e83c45e8378 cat /root/ping-result.txt
        PING 172.17.0.2 (172.17.0.2): 56 data bytes
        64 bytes from 172.17.0.2: seq=0 ttl=64 time=0.195 ms
        64 bytes from 172.17.0.2: seq=1 ttl=64 time=0.105 ms
        64 bytes from 172.17.0.2: seq=2 ttl=64 time=0.124 ms
        64 bytes from 172.17.0.2: seq=3 ttl=64 time=0.095 ms
        64 bytes from 172.17.0.2: seq=4 ttl=64 time=0.085 ms

        --- 172.17.0.2 ping statistics ---
        5 packets transmitted, 5 packets received, 0% packet loss
        round-trip min/avg/max = 0.085/0.120/0.195 ms

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occo-infra-start``
    .. code::

        occo-infra-stop --cfg conf/occo.yaml -i 6e259ac2-6f4d-4cae-8a05-f802fe5a4ac3
