.. _tutorial:

Tutorial
========

In this section, examples will be shown, how this tool can be used. Each
subsection details a certain infrastructure by which the user can learn how the
different features can be utilised.

Please, note that the following examples require a properly configured tool.

Helloworld
----------
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
The example can be downloaded from `here <http://www.lpds.sztaki.hu/services/sw/download.php?download=2f4ab6dc7fc0608501faa97e5ab9b8a0>`_.

Instructions
~~~~~~~~~~~~
The following steps are suggested to be peformed:

#. Edit ``conf/components.yaml``. Set the ``endpoint`` and the ``regionname`` of your ec2 interface to your target cloud.
    .. code::

        my_cloud:
            protocol: boto
            name: MYCLOUD
            target:
                endpoint: endpoint_of_ec2_interface_of_your_cloud
                regionname: regionname_of_your_ec2_interface

#. Edit ``conf/auth_data.yaml``. Based on your credentials, set ``username`` to the value of your ec2 access-key and set ``password`` to the value of your ec2 secret-key. 
     .. code::

        username: your_ec2_auth_key
        password: your_ec2_secret_key

#. Edit ``init_data/uds_init_data.yaml``. Set the image id for the node called ``hw_node``. Select an image containing a base os installation with cloud-init support.
     .. code::

        ... 
        image_id: id_of_your_image_on_your_target_cloud
        instance_type: instance_type_of_your_image_on_your_target_cloud
        ...

#. Load the node definition for ``helloworld`` node into the database. 
    .. code::

        cd init_data
        redisload redis_data.yaml
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

        occo-infra-stop --cfg conf/occo.yaml -i <infraid>

Ping
----


