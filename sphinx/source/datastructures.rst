.. _datastructures:

Data Structures
===============

Specification and examples of data structures used on the OCCO system.

OCCO uses simple data structures that can be expressed in :term:`YAML` scalars
(:class:`str`, :class:`int`, :data:`None`, etc.), mappings (:class:`dict`),
arrays (:class:`list`), and their recursive constructions.

Some of the scalar types OCCO utilizes are complex Python classes that can be
serialized in YAML. For example, :class:`~occo.util.factory.factory.register`
will register a YAML constructor for the specific
:class:`~occo.util.factory.factory.MultiBackend` class so the YAML parser will
automatically instantiate the correct backend for that class. This makes the
example configuration in :ref:`occo.util.factory <factory_example_config>`
possible.

.. _infradescription:

Infrastructure Description
--------------------------

Dependency graph on :ref:`nodedescription`-s.

.. todo:: The use of ``environment_id``, ``infra_id``, and
    ``infrastructure_id`` is inconsistent throughout the code and the system.
    We need to refactor the code and the design so it is consistently called
    ``infrastructure_id``. We should drop the "environment" terminology
    altogether, as it is Chef-specific.

.. _nodedescription:

Node Description
----------------

Abstract description of a node, which identifies a type of node a user may
include in an infrastructure. It is an abstract, backend-independent definition
of a class of nodes and can be stored in a repository.

This data structure does not contain information on how it can be
instantiated. Rather, it refers to one or more *implementations* that can be
used to instantiate the node. These implementations are described with
:ref:`node definition <nodedefinition>` data structures.

To instantiate a node, its implementations are gathered first. Then, they are
either filtered by ``backend_id`` (if explicitly specified), or one is selected
by some brokering algorithm (currently: randomly).

The node definition will then be resolved to a :ref:`resolved node definition
<resolvednode>` so it contains all information required by the intended
backend. For details, continue to :ref:`nodedefinition`, and then to
:ref:`resolvednode`.

  ``name``
      Uniquely identifies the node inside the infrastructure.
  ``type``
      The type of the node.
  ``backend_id``
      Optional. The dedicated backend for this node. If unspecified, the
      :ref:`Infrastructure Processor <infraprocessor>` will choose among
      implementations.
  ``environment_id``
      Back reference to the containing infrastructure instance.
  ``user_id``
      User identifier of the infrastructure instance. This is an optimization.
      The :term:`IP` could resolve this by querying the static description of
      the containing infrastructure, but it is much more efficient to simply
      copy the ``user_id`` to each node's description.

Infrastructure Static State
---------------------------

Describes the desired/ideal state of the infrastructure. Essentially a
topological ordering of the :ref:`infradescription`.

.. todo:: The specification can be foun in the code:
    :class:`occo.compiler.compiler.StaticDescription`

.. _nodedefinition:

Node Definition
---------------

Describes an *implementation* of a :ref:`node <nodedescription>`, a template
that is required to instantiate a node. The template pertains to a specific
:ref:`Cloud Handler <cloudhandler>` (through ``backend_id``), and a specific
:ref:`Service Composer <servicecomposer>` (to be implemented).

A node definition does not contain all information needed to instantiate the
data. It is just a backend-\ *dependent* description that can be stored in a
repository (cf. with :ref:`nodedescription`, which is backend-\ *independent*).

To be used to instantiate a concrete node, this template needs to be resolved;
that is, filled in with actual information. This results in a
:ref:`resolved node definition <resolvednode>` (see there for details).

    ``implementation_type``
        The :mod:`Resolver <occo.infraprocessor.node_resolution>` module uses
        this to select the correct resolver. This string should identify the
        cloud handler + service composer pair that can handle this
        implementation. E.g. ``"chef+cloudinit"``.
    ``...``
        Extra information required by the resolver handling this type of
        implementation. E.g. ``"context_template"`` in case of cloud-init
        backends.
        
.. _resolvednode:

Resolved Node Definition
------------------------

The :ref:`node definition <nodedefinition>` contains the *template* to
instantiate a node in a specific backend, but it does not contain actual
details: it must be resolved first.

The resolution in initiated by the :ref:`Infrastructure Processor
<infraprocessor>`, and performed by the :mod:`node resolution
<occo.infraprocessor.node_resolution>` module. The correct resolution algorithm
determines the content of the resolved node definition, which depends on the
backend type of the :ref:`Cloud Handler <cloudhandler>` *and* the type of the
:ref:`Service Composer <servicecomposer>`.

A resolved node definition is not intended to be stored in any permanent
storage as it is product of the :ref:`node definition <nodedefinition>` and
up-to-date information from the :ref:`Information Broker <infobroker>`.

The content of the resolved node definition depends completely on the resolving
algorithm.

.. _instancedata:

Instance Data
-------------

Specification of a running node instance. A ``(backend_id, instance_id)`` pair
is required and is sufficient to manipulate a running node instance.

    ``node_id``
        Internal identifier of the node instance.
    ``backend_id``
        Identifies the backend that has actually handled the creation of this
        node.
    ``instance_id``
        Identifier of the node instance in the backend's domain (e.g. boto vm
        id).
    ``user_id``
        User identifier of the infrastructure this node pertains to.
