.. _installation:

Setup
=====

Installation
------------

Please, perform the following steps to deploy OCCO and its dependencies in your environment:

    #. Install a few system-wide packages

        Python version ``2.7``

         * ``sudo apt-get install python``

        Virtualenv version ``12.0.7`` or later. Make *sure* that it is at least version 12. 

         * ``sudo apt-get install python-virtualenv``

        Redis server for OCCO to store persistent data

         * ``sudo apt-get install redis-server``

        SSL development libraries for the Chef connection to work

         * ``sudo apt-get install libssl-dev``

        Mysql client for PyMySQL to work

         * ``sudo apt-get install mysql-client``

    #. Prepare the environment (you may skip this part to have a system-wide installation, not recommended)

         * ``virtualenv occo``            # to create virtualenv called 'occo'
         * ``source occo/bin/activate``   # to activate virtualenv
         * ``pip install --upgrade pip``  # to make sure the latest pip version

    #. Deploy all OCCO pacakges

         * ``pip install --find-links http://pip.lpds.sztaki.hu/packages --no-index --trusted-host pip.lpds.sztaki.hu OCCO-API``
        
    Now, all OCCO packages are deployed under your virtualenv ``occo``. 

.. note::

   Do not forget to activate your virtualenv before usage!

Configuration
-------------

