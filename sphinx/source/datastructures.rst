.. _datastructures:

Data Structures
===============

Specification and examples of data structures used on the OCCO system.

OCCO uses simple data structures that can be expressed in YAML: scalars
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
