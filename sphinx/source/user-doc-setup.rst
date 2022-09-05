
Setup
=====

.. _installation:

Installation
------------

.. important::

   We primarily support **Ubuntu** operating system. The following instruction steps were tested on **Ubuntu 20.04** version.

#. Install a few system-wide packages

   Python ``3.x``, Virtualenv, Redis server for data storage and  SSL devel lib for Chef to work

   .. code:: bash

      sudo apt update && \
      sudo apt install -y python3-pip python3-dev virtualenv redis-server libssl-dev

#. Prepare the environment (you may skip this part to have a system-wide installation, not recommended)

   .. code:: bash

      virtualenv -p python3 $HOME/occopus
      source $HOME/occopus/bin/activate

#. Deploy all Occopus packages

   .. code:: bash

      pip install --no-index --find-links https://pip3.lpds.sztaki.hu/packages OCCO_API

   Now, all Occopus packages are deployed under your virtualenv ``occopus``.

#. Optionally, copy your certs under Occopus if you plan to use VOMS authentication against Nova resources

   .. code:: bash

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

.. code:: bash

   mkdir -p $HOME/.occopus
   curl https://raw.githubusercontent.com/occopus/docs/devel/tutorials/.occopus/occopus_config.yaml -o $HOME/.occopus/occopus_config.yaml

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

.. code:: bash

    mkdir -p $HOME/.occopus
    curl https://raw.githubusercontent.com/occopus/docs/devel/tutorials/.occopus/auth_data.yaml -o $HOME/.occopus/auth_data.yaml

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

  In case of application credential based authentication:

  .. code:: yaml

    resource:
        -
            type: nova
            auth_data:
                type: application_credential
                id: id_of_the_app_cred
                secret: password_of_the_app_cred

  In case of VOMS proxy authentication:

  .. code:: yaml

    resource:
        -
            type: nova
            auth_data:
                type: voms
                proxy: path_to_your_x509_voms_proxy_file

For ``azure`` resources:

.. code:: yaml

    resource:
        -
            type: azure_vm
            auth_data:
                tenant_id: your_tenant_id
                client_id: your_client_id
                client_secret: your_client_secret
                subscription_id: your_subscription_id

Please consult the `Azure Documentation <https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#get-application-id-and-authentication-key>`_ on how to obtain the necessary ``tenant_id``, ``client_id``, ``client_secret`` and ``subscription_id`` values, and how to gain proper access for being able to manage Azure virtual machines and associated resources.

For ``azure_aci`` resources:

.. code:: yaml

    resource:
        -
            type: azure_aci
            auth_data:
                tenant_id: your_tenant_id
                client_id: your_client_id
                client_secret: your_client_secret
                subscription_id: your_subscription_id

Please consult the `Azure Documentation <https://docs.microsoft.com/en-us/azure/active-directory/develop/howto-create-service-principal-portal#get-application-id-and-authentication-key>`_ on how to obtain the necessary ``tenant_id``, ``client_id``, ``client_secret`` and ``subscription_id`` values, and how to gain proper access for being able to manage Azure continer instances and associated resources.

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







