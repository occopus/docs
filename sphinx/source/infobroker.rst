Information Distribution in OCCO
================================

Example
-------
``provider.yaml``

.. code-block:: yaml

    --- !TestRouter
    sub_providers:
        - !TestProviderA
        - !TestProviderB

``inforouter_example.py``

.. code-block:: python

    import datetime
    import occo.infobroker as ib

    # For all @provider classes, a YAML constructor will be
    # defined and registered.
    #
    # In all @provider classes, @provides methods will be registered
    # as for the given key.
   
    @ib.provider
    class TestProviderA(ib.InfoProvider):

        @ib.provides("global.echo")
        def echo(self, msg, **kwargs):
            return msg

        @ib.provides("global.time")
        def gettime(self):
            return datetime.datetime.now()

    @ib.provider
    class TestProviderB(ib.InfoProvider):

        @ib.provides("global.hello")
        def hithere(self, **kwargs): # <-- ... this.
            return 'Hello World!'

    @ib.provider
    class TestRouter(ib.InfoRouter):
        pass

    # Providers and sub-providers will be automatically instantiated
    # using pre-defined YAML constructors.
    with open('config.yaml') as f
        provider = config.DefaultYAMLConfig(f)

    print provider.get("global.hello") # <- This will call ...

Abstract Information Providers
------------------------------
.. automodule:: occo.infobroker.provider
    :members:
    :special-members:
