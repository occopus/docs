.. _tutorial-building-clusters:

Tutorials on building clusters
==============================

Docker-Swarm cluster
~~~~~~~~~~~~~~~~~~~~

This tutorial sets up a complete Docker infrastructure with Swarm, Docker and Consul software components. It contains a head node and predefined number of worker nodes. The worker nodes receive the ip of the head node and attach to the head node to form a cluster. Finally, the docker cluster can be used with any standard tool talking the docker protocol (on port 2375).

**Features**

 - creating two types of nodes through contextualisation
 - passing ip address of a node to another node
 - using the occi resource handler
 - utilising health check against a predefined port
 - using parameters to scale up worker nodes

**Prerequisites**

 - accessing an Occopus compatible interface 
 - target cloud contains an Ubuntu 14.04 image with cloud-init support

**Download**

You can download the example as `tutorial.examples.docker-swarm <../../examples/docker-swarm.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Open ``nodes/node_definitions.yaml`` and edit the resource section of ``dockerswarm_head_node`` and ``dockerswarm_worker_node`` nodes. Set the followings in their ``resource`` section:

   - ``endpoint`` is an url of a CloudSigma interface of a cloud (e.g. `https://zrh.cloudsigma.com/api/2.0`).
   - ``libdrive_id`` is the image id (e.g. `40aa6ce2-5198-4e6b-b569-1e5e9fbaf488`) on your CloudSigma cloud. Select an image containing a base os installation with cloud-init support!
   - ``cpu`` is the speed of CPU (e.g. `2000`) in terms of MHz of your VM to be instantiated.
   - ``mem`` is the amount of RAM (e.g. `1073741824`) in terms of bytes to be allocated for your VM.
   - ``vnc_password`` set the password for your VNC session.
   - ``pubkeys``  optionally specifies the keypairs (e.g. `f80c3ffb-3ab5-461e-ad13-4b253da122bd`) to be assigned to your VM.
   - ``firewall_policy`` optionally specifies network policies (you can define multiple security groups in the form of a list, e.g. `8cd00652-c5c8-4af0-bdd6-0e5204c66dc5`) of your VM.

   For further explanation, read the :ref:`node definition's resource section <userdefinitionresourcesection>` of the User Guide.

   .. code::

     'node_def:dockerswarm_head_node':
         -
            resource:
                type: cloudsigma
                endpoint: replace_with_endpoint_of_cloudsigma_interface_of_your_cloud
                libdrive_id: replace_with_id_of_your_library_drive_on_your_target_cloud
                description:
                    cpu: 2000
                    mem: 1073741824
                    vnc_password: secret
                    pubkeys:
                        -
                            replace_with_id_of_your_pubkey_on_your_target_cloud
                    nics:
                        -
                            firewall_policy: replace_with_id_of_your_network_policy_on_your_target_cloud
                            ip_v4_conf:
                                conf: dhcp
             ...
     'node_def:dockerswarm_worker_node':
         -
             resource:
                type: cloudsigma
                endpoint: replace_with_endpoint_of_cloudsigma_interface_of_your_cloud
                libdrive_id: replace_with_id_of_your_library_drive_on_your_target_cloud
                description:
                    cpu: 2000
                    mem: 1073741824
                    vnc_password: secret
                    pubkeys:
                        -
                            replace_with_id_of_your_pubkey_on_your_target_cloud
                    nics:
                        -
                            firewall_policy: replace_with_id_of_your_network_policy_on_your_target_cloud
                            ip_v4_conf:
                                conf: dhcp
             ...

#. Make sure your authentication information is set correctly in your authentication file. You must set your email and password in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Load the node definition for ``dockerswarm_head_node`` and ``dockerswarm_worker_node`` nodes into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition (file) changes!

   .. code::

      occopus-import nodes/node_definitions.yaml

#. Update the number of worker nodes if necessary. For this, edit the ``infra-docker-swarm.yaml`` file and modify the ``min`` parameter under the ``scaling`` keyword. Currently, it is set to ``2``.

   .. code::

     - &W
         name: worker
         type: dockerswarm_worker_node
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
       <ip-address> (dfa5f4f5-7d69-432e-87f9-a37cd6376f7a)
     worker:
       <ip-address> (cae40ed8-c4f3-49cd-bc73-92a8c027ff2c)
       <ip-address> (8e255594-5d9a-4106-920c-62591aabd899)
     77cb026b-2f81-46a5-87c5-2adf13e1b2d3

#. Check the result by submitting docker commands to the docker head node!

#. Finally, you may destroy the infrastructure using the infrastructure id returned by ``occopus-build``

   .. code::

      occopus-destroy -i 77cb026b-2f81-46a5-87c5-2adf13e1b2d3

Hadoop cluster
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

