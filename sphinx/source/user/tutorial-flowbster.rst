.. _tutorials-for-flowbster:

Tutorials for Flowbster
=======================

Autodock vina
~~~~~~~~~~~~~

In this case we have used Flowbster to set up the infrastructure for processing the Vina workflow. The setup is as follows: one VM is acting as the Generator, 5 VMs are acting as Vina processing nodes, and finally one VM is acting as the Collector node. 


The application used to execute the performance measurements was a workflow based on the AutoDock Vina application. The workflow consists of three nodes: a Generator, a set of Vina processing nodes, and a Collector. The input of the workflow includes the followings: a receptor molecule, a Vina configuration file, and a set of molecules to dock against the receptor molecule.


The task of the generator node is to split the set of molecules to dock into a number of parts. The task of the Vina nodes is to process this parts, iterating through each molecule in the given part, by performing the docking simulation. The result of the docking includes an energy level, finally the user is interested in the docking with the lowest energy level.


The task of the Collector node is to get the processing result of each molecule part from the Vina nodes, and select the best 5 energy levels.


For running the experiment, we selected a molecule set of 60 molecules. This set was split into 10 parts, so each part included 6 molecules to dock against the receptor molecule.

**Features**

 - creating nodes through contextualisation
 - using the ec2 resource handler
 - utilising health check against a predefined port and url
 - using parameters to scale up worker nodes

**Prerequisites**

 - accessing an Occopus compatible interface
 - target cloud contains an Ubuntu 14.04 image with cloud-init support

**Download**

You can download the example as `tutorial.examples.flowbster-autodock-vina <../../examples/flowbster-autodock-vina.tgz>`_ .

**Steps**

The following steps are suggested to be performed:

#. Open the file ``nodes/node_definitions.yaml`` and edit the resource section of the flowbster_node labelled by ``node_def:``.

   - you must select an `Occopus compatible resource plugin <clouds.html>`_
   - you can find and specify the relevant `list of attributes for the plugin <createinfra.html#resource>`_
   - you may follow the help on `collecting the values of the attributes for the plugin <createinfra.html#collecting-resource-attributes>`_
   - you may find a resource template for the plugin in the `resource plugin tutorials <tutorial-resource-plugins.html>`_

   The downloadable package for this example contains a resource template for the ec2 plugin.

#. Make sure your authentication information is set correctly in your authentication file. You must set your email and password in the authentication file. Setting authentication information is described :ref:`here <authentication>`.

#. Components in the infrastructure connect to each other, therefore several port ranges must be opened for the VMs executing the components. Clouds implement port opening various way (e.g. security groups for OpenStack, etc.). Make sure you implement port opening in your cloud for the following port:

   .. code::

      TCP 5000 receiverport. This is used by nodes to handle incoming requests from other agents.

#. Please note that in order to receive the results, you have to run a Gather service (part of Flowbster), which will finally gather the results (the docking simulations with the lowest energy levels) from the Collector (last node in the workflow). Start the Gather service using the following command:

   .. code::

      scripts/flowbster-gather.sh -s

   By default the Gather service is listening on port 5001.

   .. note::

      The scripts in the scripts directory need Python 2.7. Alternatively you can activate the Occopus virtualenv!


#. Edit the “variables” section of the infra-autodock-vina.yaml file. Set the following attributes:

   - ``gather_ip`` is the ip address of the host where you have started the Gather service
   - ``gather_port`` is the port of the Gather service is listening on

   .. code::

    gather_ip: &gatherip "<External IP of the host executing the Gather service>"
    gather_port: &gatherport "5001"


#. Update the number of VINA nodes if necessary. For this, edit the ``infra-autodock-vina.yaml`` file and modify the ``min`` parameter under the ``scaling`` keyword. Currently, it is set to ``5``.

   .. code::

    - &VINA
        name: VINA
        type: flowbster_node
        scaling:
                min: 5

#. Load the node definition for ``flowbster_node`` nodes into the database.

   .. important::

      Occopus takes node definitions from its database when builds up the infrastructure, so importing is necessary whenever the node definition (file) changes!

   .. code::

      occopus-import nodes/node_definitions.yaml


#. Start deploying the infrastructure. Make sure the proper virtualenv is activated!

   .. code::

      occopus-build infra-autodock-vina.yaml

#. After successful finish, the nodes with ``ip address`` and ``node id`` are listed at the end of the logging messages and the identifier of the newly built infrastructure is printed. You can store the identifier of the infrastructure to perform further operations on your infra or alternatively you can query the identifier using the **occopus-maintain** command.

   .. code::

     List of nodes/ip addresses:
     VINA:
       <ip-address> (2f7d3d7e-c90c-4f33-831d-91e987e8e8b2)
       <ip-address> (49bed8d2-94b0-4a7e-9672-744921dacac0)
       <ip-address> (10664026-0b31-4848-9f7a-98f880f98be7)
       <ip-address> (a0f5d091-aecc-488c-94f2-34e546f87832)
       <ip-address> (285d7efd-84a7-4ed5-a6fa-73db47bc2e87)
     COLLECTOR:
       <ip-address> (4ca11ad3-a6ec-411b-89e6-d516169df9c7)     
     GENERATOR:
       <ip-address> (9b8dc4f1-bed4-4d1c-ba9e-45c18ee2523d)
     30bc1d09-8ed5-4b7e-9e51-24ed881fc166

#. Once the infrastructure is ready, the input files can be sent to the Generator node of the workflow (check the address of the node at the end of the output of the  **occopus-build** command). Using the following command in the ``flowbster-autodock-vina/inputs`` directory:

   .. code::

     ../scripts/flowbster-feeder.sh -h <ip of GENERATOR node> -i input-description-for-vina.yaml -d input-ligands.zip -d input-receptor.pdbqt -d vina-config.txt

   The -h parameter is the Generator node’s address, -i is the input description file and with -d we can define data file(s).

   .. note::

      The scripts in the scripts directory need Python 2.7. Alternatively you can activate the Occopus virtualenv!


   .. note::

      It may take a quite few minutes until the processes end. Please, be patient!


#. With step 10, the data processing was started. The whole processing time depends on the overall performance of the VINA nodes. VINA nodes process 10 molecule packages, which are collected by the Collector node. You can check the progress of processing on the Collector node by checking the number of files under ``/var/flowbster/jobs/<id of workflow>/inputs`` directory. When the number of files reaches 10, Collector node combines them and sends one package to Gather node which stores it under directory ``/tmp/flowbster/results``. 

#. Once you finished processing molecules, you may stop the Gather service:

   .. code::

      scripts/flowbster-gather.sh -d

#. Finally, you can destroy the infrastructure using the infrastructure id returned by **occopus-build**


   .. code::

      occopus-destroy -i 30bc1d09-8ed5-4b7e-9e51-24ed881fc166


.. note::

  You can run a bigger application, with more input files. This application will run for approximately 4 hours with 5 VINA nodes. Edit Generator node's variables section in the ``infra-autodock-3node.yaml`` file. Set the ``jobflow/app/args`` variable 10 to ``240`` and repeat the tutorial using the ``input2`` directory. For running this experiment, we selected a molecule set of 3840 molecules. This set will be splitted into 240 parts, so each part included 16 molecules to dock against the receptor molecule.

  .. code::

    nodes:
        - &GENERATOR
            name: GENERATOR
            type: flowbster_node
            variables:
                flowbster:
                    app:
                        exe:
                            filename: execute.bin
                            tgzurl: https://github.com/occopus/flowbster/raw/master/examples/vina/bin/generator_exe.tgz
                        args: '240'


