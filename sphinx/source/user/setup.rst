
Setup
=====

.. _installation:

Installation
------------

The steps required to deploy Occopus and its dependencies are described below. Alternatively, you can watch a `video on installing Occopus v1.2 <http://smith.s3.lpds.sztaki.hu/Occopus/occopus_v1.2_installation.mp4>`_ .

#. Install a few system-wide packages

   Python version ``2.7`` and two devel libs for dependencies

   .. code:: yaml
         
    sudo apt-get install python python-dev libffi-dev

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

Occopus requires one configuration file containing static parameters and objects to be instantiated when Occopus starts. The file is ``occopus_config.yaml``.

This file must be specified for Occopus through command line parameters. Alternatively, we recommend to store this file in ``$HOME/.occopus`` directory, so that Occopus will automatically find and use it.

Please, download and save your configuration file:

.. code:: yaml

   mkdir -p $HOME/.occopus
   curl https://raw.githubusercontent.com/occopus/docs/devel/tutorial/.occopus/occopus_config.yaml -o $HOME/.occopus/occopus_config.yaml

Occopus uses YAML as a configuration language, mainly for its dynamic properties, and its human readability. The parsed configuration is a dictionary, containing both static parameters and objects instantiated by the YAML parser.

.. note::

   Please, do not modify the configuration file unless you know what you are doing!

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

For ``EC2`` resources:

.. code:: yaml

    resource:
        -
            type: ec2
            auth_data:
                accesskey: your_access_key
                secretkey: your_secret_key

For ``nova`` resources:

  In case of username/password authentication:

  .. code:: yaml
    
    resource:
        -
            type: nova
            auth_data:
                username: your_username
                password: your_password

  In case of VOMS proxy authentication:

  .. code:: yaml
    
    resource:
        -
            type: nova
            auth_data:
                type: voms
                proxy: path_to_your_x509_voms_proxy_file

For ``occi`` resources:

.. code:: yaml

    resource:
        -
            type: occi
            auth_data:
                proxy: path_to_your_voms_proxy_file

For ``cloudbroker`` resources:

.. code:: yaml

    resource:
        -
            type: cloudbroker
            auth_data:
                email: your@email.com
                password: your_password

For ``cloudsigma`` resources:

.. code:: yaml

    resource:
        -
            type: cloudsigma
            auth_data:
                email: your@email.com
                password: your_password


For ``chef`` config managers:

.. code:: yaml

    config_management:
        -
            type: chef
            auth_data:
                client_name: name_of_user_on_chef_server
                client_key: !text_import
                    url: file://path_to_the_pem_file_of_cert_for_user

The values for ``client_name`` and ``client_key`` attributes must be the name of the **user** that can login to the Chef server and the public key of that Chef user. This user and its key will be used by Occopus to register the infrastructure before deployment of nodes starts. As the example shows above, the key can be imported from a separate file, so the path to the **pem** file is enough to be specified in the last line.

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

For multiple resources with different endpoints:

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







