.. _tutorial:

Tutorial
========

In this section, examples will be shown, how this tool can be used. Each
subsection details a certain infrastructure by which the user can learn how the
different features can be utilised.

Please, note that the following examples require a properly configured tool.

EC2-Helloworld
--------------
This tutorial sets up an infrastructure containing a single node. The node will
receive information (i.e. a message string) through contextualisation. The node
will store this information in ``/tmp`` directory.

Features
~~~~~~~~
In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

Prerequisites
~~~~~~~~~~~~~
 - accessing a cloud through EC2 interface (access key, secret key, endpoint, regionname)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

Download
~~~~~~~~
You can download the example as `tutorial.examples.ec2-helloworld <https://www.lpds.sztaki.hu/services/sw/download.php?download=73672d0086bb4493fdf8dd29c0dbb0d1>`_ .

Instructions
~~~~~~~~~~~~
The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
    .. code::

        my_cloud:
            protocol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key. 
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for the node called ``hw_node``. Select an image containing a base os installation with cloud-init support.
     .. code::

        ... 
        image_id: replace_with_id_of_your_image_on_your_target_cloud
        instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
        ...

#. Load the node definition for ``helloworld`` node into the database. 
    .. code::

        cd init_data
        occo-import-node redis_data.yaml
        cd ..

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

Features
~~~~~~~~
In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

Prerequisites
~~~~~~~~~~~~~
 - accessing a cloud through EC2 interface (access key, secret key, endpoint, regionname)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

Download
~~~~~~~~
You can download the example as `tutorial.examples.ec2-ping <https://www.lpds.sztaki.hu/services/sw/download.php?download=97a95c3739811463b7c37d197afd650d>`_ .

Instructions
~~~~~~~~~~~~
The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
    .. code::

        my_cloud:
            protocol: boto
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                regionname: replace_with_regionname_of_your_ec2_interface

#. Edit or create ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key. 
     .. code::

        username: replace_with_your_ec2_auth_key
        password: replace_with_your_ec2_secret_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id (e.g. ``ami-12345678``) and instance_type (e.g. ``m1.small``) for the nodes called ``ping_receiver_node`` and ``ping_sender_node``. Select an image containing a base os installation with cloud-init support.
     .. code::

        'node_def:ping_receiver_node':
            ... 
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
            ...
        'node_def:ping_sender_node':
            ...
            image_id: replace_with_id_of_your_image_on_your_target_cloud
            instance_type: replace_with_instance_type_of_your_image_on_your_target_cloud
            ...

#. Load the node definition for ``ping-receiver`` and ``ping-sender`` nodes into the database. 
    .. code::

        cd init_data
        occo-import-node redis_data.yaml
        cd ..

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

Features
~~~~~~~~
In this example, the following feature(s) will be demonstrated:
 - creating a node with minimal setup
 - passing information to a target node

Prerequisites
~~~~~~~~~~~~~
 - accessing an OpenStack cloud through Nova interface (access key, secret key, endpoint, tenant name)
 - target cloud contains a base OS image with cloud-init support (image id, flavor)

Download
~~~~~~~~
You can download the example as `tutorial.examples.nova-helloworld <https://www.lpds.sztaki.hu/services/sw/download.php?download=73672d0086bb4493fdf8dd29c0dbb0d1>`_ .

Instructions
~~~~~~~~~~~~
The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``tenant_name`` of your Nova interface to your target cloud.
    .. code::

        my_cloud:
            protocol: nova
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_nova_interface_of_your_cloud
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

        cd init_data
        occo-import-node redis_data.yaml
        cd ..

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

Features
~~~~~~~~
In this example, the following feature(s) will be demonstrated:
 - creating two nodes with dependencies (i.e ordering or deployment)
 - querying a node's ip address and passing the address to another

Prerequisites
~~~~~~~~~~~~~
 - accessing an OpenStack cloud through Nova interface (access key, secret key, endpoint, tenant name)
 - target cloud contains a base OS image with cloud-init support (image id, flavour)

Download
~~~~~~~~
You can download the example as `tutorial.examples.nova-ping <https://www.lpds.sztaki.hu/services/sw/download.php?download=97a95c3739811463b7c37d197afd650d>`_ .

Instructions
~~~~~~~~~~~~
The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``tenant_name`` of your Nova interface to your target cloud.
    .. code::

        my_cloud:
            protocol: nova
            name: MYCLOUD
            target:
                endpoint: replace_with_endpoint_of_nova_interface_of_your_cloud
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

        cd init_data
        occo-import-node redis_data.yaml
        cd ..

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


