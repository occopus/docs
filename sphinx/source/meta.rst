.. _metadocs:

Meta-Documentation -- Sphinx plugin to autodoc InfoBroker keys
==============================================================

Info Broker Keys
----------------

The query keys provided by the :ref:`Info Broker <infobroker>` are documented,
and an index is created, automatically from the code.

For this, an extension for Sphinx has been developed, providing three
directives:

    ``.. decl_ibkey::``
        
        This directive is prepended to all documented methods automatically,
        by the :class:`@provides <occo.infobroker.provider.provides>`
        decorator. It declares the provided key in the scope of the docstring;
        developers need not bother with it.

    ``.. ibkey::``

        This directive can be used to specify query key documentation. The
        documentation inside this directive will be rendered in both the method
        documentation and the key catalog.

        It has a required argument: the one-liner synopsis of the key.

        The required parameters should be documented using ``:param ...:``
        fields.

    ``.. ibkeylist::``

        This directive will be replaced with the alphabetically sorted catalog
        of all the keys documented throughout the code.

Example
~~~~~~~

.. code:: python

    @provides('node.state')
    def query_state(self, instance_data, **kwargs):
        """
        This part of the documentation will not be rendered in the catalog.

        .. ibkey::
            Query the state of an infrastructure node.
            
            :param dict instance_data: Data required to identify the node.

            This block will be rendered in both the method documentation and
            the key catalog.

        This part of the documentation will not be rendered in the catalog
        either.
        """
        pass
