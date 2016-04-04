
Setup
=====

.. _installation:

Installation
------------

Please, perform the following steps to deploy Occopus and its dependencies in your environment:

#. Install a few system-wide packages

   Python version ``2.7``

   .. code:: yaml
         
    sudo apt-get install python

   Virtualenv version ``12.0.7`` or later. Make *sure* that it is at least version 12. 

   .. code:: yaml

    sudo apt-get install python-virtualenv

   Redis server for Occopus to store persistent data

   .. code:: yaml

    sudo apt-get install redis-server

   SSL development libraries for the Chef connection to work

   .. code:: yaml

    sudo apt-get install libssl-dev

   Mysql client for PyMySQL to work

   .. code:: yaml

    sudo apt-get install mysql-client

#. Prepare the environment (you may skip this part to have a system-wide installation, not recommended)

   .. code:: yaml

    virtualenv occopus          # to create virtualenv called 'occopus'
    source occopus/bin/activate # to activate virtualenv
    pip install --upgrade pip   # to make sure the latest pip version

#. Deploy all Occopus packages

   .. code:: yaml

    pip install --find-links http://pip.lpds.sztaki.hu/packages --no-index --trusted-host pip.lpds.sztaki.hu OCCO-API

   Now, all Occopus packages are deployed under your virtualenv ``occopus``. 

#. Optionally, copy your certs under Occopus if you plan to use VOMS authentication against OCCI or Nova resources

   .. code:: yaml

    cat /etc/grid-security/certificates/*.pem >> $(python -m requests.certs)

.. note::

   Do not forget to activate your virtualenv before usage!

.. note::

   Please, proceed to the next chapter to continue with configuration!

Configuration
-------------

Occopus requires 2 basic configuration files:

#. ``occopus_config.yaml`` : contains static parameters and objects to be instantiated when Occopus starts

#. ``redis_config.yaml`` : contains parameters for accessing the redis key-value store

These files must be specified for Occopus through command line parameters. Alternatively, we recommend to store these files in ``$HOME/.occopus`` directory, so that Occopus will automatically find and use it.

Please, download and save your configuration files:

.. code:: yaml

   mkdir -p $HOME/.occopus
   curl https://raw.githubusercontent.com/occopus/docs/devel/tutorial/.occopus/occopus_config.yaml -o $HOME/.occopus/occopus_config.yaml
   curl https://raw.githubusercontent.com/occopus/docs/devel/tutorial/.occopus/redis_config.yaml -o $HOME/.occopus/redis_config.yaml

Occopus uses YAML as a configuration language, mainly for its dynamic properties, and its human readability. The parsed configuration is a dictionary, containing both static parameters and objects instantiated by the YAML parser.

.. note::

   Please, do not modify the configuration files unless you know what you are doing!

.. note::

   Please, proceed to the next chapter to continue with setting up authentication information!

.. _authentication:

Authentication
--------------

**Authentication file**

In order to get access to a resource, Occopus requires your credentials to be defined. For this purpose you have to create a file, ``auth_data.yaml`` containing authentication information for each target resource in a structured way.

Once you have your ``auth_data.yaml``  file, you must specify it as command line argument for Occopus. A more convenient (recommended) way is to save this file at ``$HOME/.occopus/auth_data.yaml`` so that Occopus will automatically find and use it.

You can download and save your initial authentication file:

.. code:: yaml

    mkdir -p $HOME/.occopus
    curl https://raw.githubusercontent.com/occopus/docs/devel/tutorial/.occopus/auth_data.yaml -o $HOME/.occopus/auth_data.yaml

Once you have your initial authentication file, edit and insert your credentials to the appropriate section.

For each different type of resources, you may specify different authentication information, which must fit to the format required by the resource plugin defined by the type keyword. Here are the formats for the different resource types.

**Authentication data formats**

For ``EC2`` resource:

.. code:: yaml

    resource:
        -
            type: ec2
            auth_data:
                accesskey: your_access_key
                secretkey: your_secret_key

For ``nova`` resource:

.. code:: yaml
    
    resource:
        -
            type: nova
            auth_data:
                type: voms
                proxy: path_to_your_voms_proxy_file

For ``occi`` resource:

.. code:: yaml

    resource:
        -
            type: occi
            auth_data:
                proxy: path_to_your_voms_proxy_file

For ``cloudbroker`` resource:

.. code:: yaml

    resource:
        -
            type: cloudbroker
            auth_data:
                email: your@email.com
                password: your_password

For ``docker`` resource:

.. code:: yaml

    resource:
        -
            type: docker
            auth_data: unused


For ``chef`` config manager:

.. code:: yaml

    config_management:
        -
            type: chef
            auth_data:
                client_name: name_of_client_on_chef_server
                client_key: !text_import
                    url: file://path_to_the_pem_file_of_cert_for_client


For multiple resource types:

.. code:: yaml

    resource:
        -
            type: ec2
            auth_data:
                accesskey: your_access_key
                secretkey: your_secret_key
        -
            type: nova
            auth_data:
                type: voms
                proxy: path_to_your_voms_proxy_file

For multiple resources on different endpoints:

.. code:: yaml

    resource:
        -
            type: ec2
            endpoint: my_ec2_endpoint_A
            auth_data:
                accesskey: your_access_key_for_A
                secretkey: your_secret_key_for_A
        -
            type: ec2
            endpoint: my_ec2_endpoint_B
            auth_data:
                accesskey: your_access_key_for_B
                secretkey: your_secret_key_for_B

.. note::

    The authentication file has YAML format. Make sure you are using spaces instead of tabulators for indentation!







