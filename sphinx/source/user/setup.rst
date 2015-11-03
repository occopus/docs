.. _installation:

Setup
=====

Installation
------------

Please, perform the following steps to deploy Occopus and its dependencies in your environment:

    #. Install a few system-wide packages

        Python version ``2.7``

         * ``sudo apt-get install python``

        Virtualenv version ``12.0.7`` or later. Make *sure* that it is at least version 12. 

         * ``sudo apt-get install python-virtualenv``

        Redis server for Occopus to store persistent data

         * ``sudo apt-get install redis-server``

        SSL development libraries for the Chef connection to work

         * ``sudo apt-get install libssl-dev``

        Mysql client for PyMySQL to work

         * ``sudo apt-get install mysql-client``

    #. Prepare the environment (you may skip this part to have a system-wide installation, not recommended)

         * ``virtualenv occo``            # to create virtualenv called 'occo'
         * ``source occo/bin/activate``   # to activate virtualenv
         * ``pip install --upgrade pip``  # to make sure the latest pip version

    #. Deploy all Occopus packages

         * ``pip install --find-links http://pip.lpds.sztaki.hu/packages --no-index --trusted-host pip.lpds.sztaki.hu OCCO-API``
        
    Now, all Occopus packages are deployed under your virtualenv ``occo``. 

.. note::

   Do not forget to activate your virtualenv before usage!

Configuration
-------------

This section is suggested to be read after some of the basic :ref:`examples of the tutorial section <tutorial>` have been successfully executed. The main purpose of this section is to provide an explanation of the configuration the examples contain.

Occopus uses YAML as a configuration language, mainly for its dynamic properties, and its human readability. The parsed configuration is a dictionary, containing both static parameters and objects already instantiated (or executed, sometimes!) by the YAML parser.

The configuration must contain the following items.

``plugins``

    List of python modules Occopus is going to use during its operation. For a basic list, see the configuration in :ref:`one of the tutorial examples <tutorial>` or use this:

    .. code::

        occo.yaml:
            plugins: !python_import
                - occo.infobroker
                - occo.infobroker.dynamic_state_provider
                - occo.infobroker.uds
                - occo.infobroker.rediskvstore
                - occo.cloudhandler
                - occo.plugins.cloudhandler.boto
                - occo.plugins.cloudhandler.nova
                - occo.plugins.cloudhandler.cloudbroker
                - occo.plugins.infraprocessor.basic_infraprocessor
                - occo.plugins.infraprocessor.node_resolution.chef_cloudinit
                - occo.plugins.infraprocessor.node_resolution.cloudbroker
                - occo.infraprocessor.synchronization.primitives
                - occo.servicecomposer
                - occo.plugins.servicecomposer.chef

    .. note::

        This part of the configuration contains all currently supported backends,
        service composers and node resolvers. Some may be useless for certain use
        cases.

``logging``

    Contains configuration for the ``Logging facility of Python``. Settings in this part of the configuration has effect on the way, location and format of the information the logger component in the various Occopus components emits. 

    For detaild explanation of the various attributes please read the `Manual for Logging facility for Python <https://docs.python.org/2/library/logging.html#module-logging>`_. Settings in this part of the configuration has effect on the location, format, etc. of the internal messages the loggeris in the various Occopus components emit during its operation.

    A sample configuration file can be found in :ref:`any of the tutorial examples <tutorial>`. Alternatively, use this basic configuration:

    .. code::

        occo.yaml:
            logging: !yaml_import
                url: file://logging.yaml
    
        logging.yaml:
            version: 1
            root:
                level: DEBUG
                handlers: [console, file]
            formatters:
                simpleFormater:
                    format: "** %(asctime)s\t%(levelname)s\t%(processName)s\t%(message)s"
    
            handlers:
                console:
                    class: logging.StreamHandler
                    formatter: simpleFormater
                    level: DEBUG
                    stream: ext://sys.stdout
                file:
                    class : logging.FileHandler
                    formatter: simpleFormater
                    mode: w
                    level: DEBUG
                    filename: rabbit.log
                datafile:
                    class : logging.FileHandler
                    formatter: simpleFormater
                    mode: w
                    level: DEBUG
                    filename: rabbit-data.log
    
            loggers:
                pika:
                    propagate: false
                    level: ERROR
                    handlers: [console]
                occo:
                    propagate: false
                    level: DEBUG
                    handlers: [console, file]
                occo.data:
                    propagate: false
                    level: DEBUG
                    handlers: [datafile]
                occo.infobroker.kvstore:
                    propagate: false
                    level: INFO
                    handlers: [console, file]
            
``components``

    The components of the Occopus architecture that’s need to be built.

    ``cloudhandler``
        
    The ``CloudHandler`` instance (singleton) is a component responsible for interacting with the cloud interface (e.g. EC2, Nova, etc.) of the target cloud. One or multiple instances can be defined i.e. Occopus can deploy infrastructures containing resources from more than one cloud. A multi-vm configuration can be realised the following way:

    .. code::

        occo.yaml:
            components: !yaml_import
                url: file://components.yaml

        components.yaml
            cloudhandler: !CloudHandler &ch
            protocol: null
            cloud_cfgs:
                my_cloud_with_ec2:
                    protocol: boto
                    name: MYEC2CLOUD
                    target:
                        endpoint: replace_with_endpoint_of_ec2_interface_of_your_cloud
                        regionname: replace_with_regionname_of_your_ec2_interface
                    auth_data: !yaml_import
                        url: file://auth_data_ec2.yaml # put your credentials here
                my_cloud_with_nova:
                    protocol: nova
                    name: MYNOVACLOUD
                    target:
                        endpoint: replace_with_endpoint_of_nova_interface_of_your_cloud
                        tenant_name: replace_with_tenant_to_use
                    auth_data: !yaml_import
                        url: file://auth_data_ec2.yaml # put your credentials here
    
    ``servicecomposer``

    The ``ServiceComposer`` instance is a component responsible for interacting with a facility that is able to build up and configure complex services and software components on the target resource. If you do not need any service configuration manager, create a *dummy* instance. You can do it with the following way:

    .. code::

        components.yaml:
            servicecomposer: !ServiceComposer &sc
                protocol: dummy

    If you would like to use chef, instantiate the chef service composer the following way:

    .. code::

        components.yaml:
            servicecomposer: !ServiceComposer &sc
                protocol: chef
                url: replace_with_endpoint_of_you_chef_server
                client: replace_with_the_username_to_your_chef_server
                key: !text_import
                    url: file://occo-test.pem #contains athentication key to chef server

    ``uds``

    The ``UDS`` (Universal Data Storage) instance is a component responsible for storing persistent data for Occopus to operate properly. The default configuration which works with `redis databases <http://redis.io>`_ are as follows:

    .. code::

        components.yaml:
            uds: !UDS &uds
                protocol: redis
                altdbs:
                    node_def: 1
                    infra: 10

    .. note::

        Please, do not change the above configuration unless you are aware of what you are doing.
     
    ``infobroker``

    The ``Information Broker`` is a component providing a simple interface for serving data by any components in the Occopus architecture. The modules serving as information provider can then be congregated into a hierarchy to realise a distributed architecture of information provider components. In Occopus, all the components are information provider in this architecture, therefore the default configuration is as follows:

    .. code::
        
        components.yaml:
            infobroker: !InfoRouter
            sub_providers:
                - !DynamicStateProvider
                    cloud_handler: *ch
                    service_composer: *sc
                - !CloudHandlerProvider
                    cloud_handler: *ch
                - *uds
                - !SynchronizationProvider
                - *sc

    .. note::

        Please, do not change the above configuration unless you are aware of what you are doing.
    
To have a full configuration, please copy the configuration parts detailed above together or download :ref:`any of the tutorial examples <tutorial>` where the configuration is slightly optimised for the infrastructure, too. 
