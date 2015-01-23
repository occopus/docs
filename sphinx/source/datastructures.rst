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

  ``name``
      Uniquely identifies the node inside the infrastructure.
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
