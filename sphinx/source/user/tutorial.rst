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

