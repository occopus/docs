.. _createinfra:

Composing an infrastructure
===========================

.. _cloudinit site: https://cloudinit.readthedocs.org/en/latest

In order to deploy an infrastructure, OCCO requires 
 #. description of the infrastructure
 #. description and definition of the individual nodes
  
The following section explains how the various descriptions must be formatted.

.. _userinfradescription:

Infrastructure Description
--------------------------

Dependency graph on :ref:`usernodedescription`-s.

The graph contains the following information:

    ``user_id``
        The identifier of the owner of the infrastructure instance.
    ``name``
        The name of the infrastructure.
    ``nodes``
        List of node.
    ``dependencies``
        List of edge definitions. Each of these can be either

            - A pair (2-list) of node references.

            - A mapping containing:

                ``connection``
                    The pair (2-list) of node references.

                ``mappings``
                    List of attribute mappings. Each mapping can be

                        - A pair (2-list) of strings (attribute specifications,
                          dotted strings permitted).

                        - A mapping containing:

                            ``attributes``
                                The pair of attribute specifications.
                            ``synch``
                                Whether to synchronize on the availability of
                                the source attribute.
                            ``**``
                                Anything else that is required by mediating
                                services.
                ``**``
                    Anything else that is required by mediating services.

    ``variables``

        Arbitrary mapping containing infrastructure-wide information. This
        information is static (not parsed anywhere). Nodes will inherit these
        variables, but they may also override them.

The following example describes a Diamond architecture.

.. code:: yaml

    user_id: 1
    name: diamond
    nodes: &NODES
        - &A
            name: A
            type: mysql-something
        - &B
            name: B
            type: wordpress-something
            scaling:
                max: 5
        - &C
            name: C
            type: something-something-darkside
            scaling:
                min: 2
                max: 5
        - &D
            name: D
            type: yaay
    dependencies:
        - [ *D, *C ]
        -
            connection: [ *D, *B ]
            mappings:
                - [ 'service.from_attribute', 'to_attribute' ]
                -
                    attributes: [ 'attrX', 'node.attribute.Y' ]
                    synch: true
                    extra: information
            extra_connection_property: 1
        - [ *B, *A ]
        - [ *C, *A ]

.. _usernodedescription:

Node Description
----------------

Abstract description of a node, which identifies a type of node a user may
include in an infrastructure. It is an abstract, *backend-independent*
definition of a class of nodes and can be stored in a repository.

A node description is self-contained in the sense that a node description
contains all the information needed to *resolve* it (i.e., in relational terms:
it does not need to be "joined" with the containing infrastructure).

This data structure does *not* contain information on how it can be
instantiated. It rather contains *what* needs to be instantiated, and under
what *conditions*. It refers to one or more *implementations* that can be used
to instantiate the node. These implementations are described with :ref:`node
definition <usernodedefinition>` data structures.

To instantiate a node, its implementations are gathered first. Then, they are
either filtered by ``backend_ids`` (if explicitly specified), or one is
selected by some brokering algorithm (currently: randomly).

    ``name``
        Uniquely identifies the node inside the infrastructure.

    ``type``
        The type of the node.

    ``backend_id`` (``str``) and ``backend_ids`` (``list``)
        Optional. The dedicated backend for this node. If unspecified, the
        :ref:`Infrastructure Processor <infraprocessor>` will choose among
        implementations.

    ``environment_id``
        Back reference to the containing infrastructure instance.

    ``user_id``
        User identifier of the infrastructure instance. This is an
        optimization.  The :term:`IP` could resolve this by querying the static
        description of the containing infrastructure, but it is much more
        efficient to simply copy the ``user_id`` to each node's description.

    ``attributes``
        Nested mappings specifying node attributes.

    ``mappings``
        Mapping specifying node attribute mapping, inbound and outbound. The
        keys of the mapping are the names of the nodes this node is connected
        with. The values of the mapping are lists containing mapping
        specifications:

            ``inbound``
                List of inbound mappings; that is, mappings this node depends
                on.

            ``outbound``
                List of outbound mappings; that is, mappings through which
                node provides information. The InfrProcessor may synchronize
                on these mappings.

            Each mapping contains a pair of ``attributes`` to be connected, the
            specification whether the IP must synchronize upon this mapping
            (``synch``), and possibly other information used by specialized
            intermediate services in the future. 

    ``variables``
        Arbitrary mapping containing static node-level information:

        #. Inherited from the infrastructure.
        #. Overridden/specified in the node's description in the
           infrastructure description.

        The final list of variables is assembled by the Compiler

.. _usernodedefinition:

Node Definition
---------------

Describes an *implementation* of a :ref:`node <usernodedescription>`, a template
that is required to instantiate a node. 

A node definition does not contain all information needed to instantiate the
data. It is just a backend-\ *dependent* description that can be stored in a
repository (cf. with :ref:`usernodedescription`, which is backend-\ *independent*).

    ``implementation_type``
        The :mod:`Resolver <occo.infraprocessor.node_resolution>` module uses
        this to select the correct resolver. This string should identify the
        cloud handler + service composer pair that can handle this
        implementation. E.g. ``"chef+cloudinit"``.
    ``backend_id``
        Refers to the cloud handler backend instance which can handle this node. OCCO
        configuration must contain a cloud handler definition having this value
        as one of its **cloud handler instance**.
    ``service_composer_id``
        Refers to the service composer which can handle this node. OCCO
        configuration must contain a service composer definition having this value
        as its **service composer instance**.
    ``...``
        Extra information required by the resolver handling this type of
        implementation. E.g. ``"context_template"`` in case of cloud-init
        backends.

Implementation-dependent attributes 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

boto
^^^^

    ``image_id``
        The identifier of the image behind the cloud handled by the cloud
        handler selected through the **backend_id** attribute.
    ``instance_type``
        The type of instance to be instantiated through EC2 when realising this
        node. This value refers to a flavour (e.g. m1.small) of the target cloud. 
        It determines the resources (CPU, memory, storage, networking) of the node. 

nova
^^^^

    ``image_id``
        The identifier of the image behind the cloud handled by the cloud
        handler selected through the **backend_id** attribute.
    ``flavor_name``
        The type of flavor to be instantiated through Nova when realising this
        node. This value refers to a flavour (e.g. m1.small) of the target cloud.
        It determines the resources (CPU, memory, storage, networking) of the node.
    ``key_name``
        The name of the keypair to be associated to the instance.
    ``security_groups``
        List of security groups to be associated to the instance.
    ``floating_ip``
        If defined (with any value), new floating IP address will be allocated
        and assigned for the instance.

chef+cloudinit
^^^^^^^^^^^^^^

    ``context_template``
        This section can contain a cloud init configuration template. It must
        follow the syntax of cloud-init. See the `Cloud-init website <cloudinit site>`_ for examples
        and details.


cloudbroker
^^^^^^^^^^^

    ``template_files``
        A list of file templates. These templates will be actualized, and passed
        as input files to the jobs instantiated. The following attributes must
        be defined:

            ``file_name``
                The name of the file. This name will be used to upload the
                actualized content.
            ``content_template``
                This section contains the template.

    ``attributes``
        The attributes defined here specify the VM image to be started up on a selected cloud
        infrastructure. In order to determine the values for the below enumerated attributes, one
        needs to log in to the CloudBroker service's web interface and collect the values.

            ``software_id``
                The ID of the CloudBroker Software to use.
            ``executable_id``
                The ID of the CloudBroker Executable to use.
            ``resource_id``
                The ID of the CloudBroker Resource (cloud) to use.
            ``region_id``
                The ID of the CloudBroker Region (cloud region) to use.
            ``instance_id``
                The ID of the CloudBroker Instance to use.


Examples
~~~~~~~~

**Example1**

- implementation_type is ``chef+cloudinit``
- backend_id points to a ``boto`` type handler
- service_composer_id poits to ``dummy`` type composer

.. code:: yaml

    uds_init_data.yaml:
        'node_def:my_node':
            -
                implementation_type: chef+cloudinit
                backend_id: my_cloud
                service_composer_id: dummy
                image_id: ami-00001234
                instance_type: m1.small
                context_template: !text_import
                        url: file://my_cloudinit_config_file.yaml

    my_cloudinit_config_file.yaml:
        #cloud-config
        write_files:
        - content: "something important static data"
          path: /tmp/my_data.txt
          permissions: '0644'

**Example2**

- implementation_type is ``cloudbroker``
- backend_id points to a ``cloudbroker`` type handler
- service_composer_id poits to ``dummy`` type composer

.. code:: yaml

    uds_init_data.yaml:
        'node_def:cloudbroker_node':
            -
                implementation_type: cloudbroker
                backend_id: cloudbroker
                service_composer_id: dummy
                template_files:
                        -
                            file_name: input1.yaml
                            content_template: !text_import
                                url: file://input1_template.yaml
                        -
                            file_name: data.yaml
                            content_template: !text_import
                                url: file://data.yaml

    input1_template.yaml:
        This is the data to be passed.

    data.yaml:
        Some more important data.
