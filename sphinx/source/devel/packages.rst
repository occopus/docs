.. _packages:

Developer information
=====================

.. _nosetests: https://nose.readthedocs.org
.. _virtualenv site: https://virtualenv.pypa.io
.. _Sphinx: http://sphinx-doc.org/
.. _Occopus Website: http://occopus.lpds.sztaki.hu

*Always* use ``virtualenv`` for any kind of deployment (testing, building,
production, ... everything). This ensures there will be no dependency issues:
deployment collisions, missing dependencies in releases, etc. See the
`virtualenv site`_ for details.

Build environment
-----------------

.. _cbe:

Creating the build environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The OCCO packages are intended to be used in ``virtualenv`` under all
circumstances. This implies that:

    #. There are only a few system-wide packages needed:

        If you experience any obscure problem during deployment, make sure that
        these versions are okay:
        
         * ``pip`` version ``6.0.8`` or later. Make *sure* that it is at least
           version 6. Older versions may complain about packages not being Zip
           files.

           Version ``7`` will complain about ``pip.lpds.sztaki.hu`` not being a
           trusted host. You can use the ``--trusted-host
           pip.lpds.sztaki.hu`` switch with ``pip``.

         * ``virtualenv`` version ``12.0.7`` or later. Make *sure* that it is
           at least version 12. One can use any one of these methods:

            * ``sudo apt-get install python-virtualenv``
            * ``sudo easy_install virtualenv``
            * ``sudo pip install --upgrade virtualenv``

         * git

         * Python **2.7**

         These are required for testing, and may be required for deployment
         too:

         * ``sudo apt-get install redis-server``
         * ``sudo apt-get install rabbitmq-server``

    #. The following are required *globally* for the MySQL-Wordpress demo to work:

        * ``sudo apt-get install libssl-dev``   # For the Chef connection to work.
        * ``sudo apt-get install mysql-client`` # For PyMySQL

    #. For the *tests* to work, you need to configure RabbitMQ

        .. code:: bash
            
            rabbitmqctl add_user test test
            rabbitmqctl add_vhost test
            rabbitmqctl set_permissions -p test test .\* .\* .\*

    #. All packages must declare all of their dependencies explicitly, without
       relying on implicit dependencies thought to be ubiquitous (e.g.
       argparse). (Because virtualenv-s are almost empty by default, containing
       only ``python`` and ``pip``.) Use ``pip freeze`` to make sure that
       everything is in order.

Git submodules can be used to clone and manage all repositories at once:

.. code:: bash

    git clone git@github.com:occopus/master.git my-occo-dir --recursive
    cd my-occo-dir
    git submodule foreach git checkout devel

Most scripts included in these components rely on **this exact directory
structure** (especially testing and documentation dependencies).

There is a Vagrantfile to bootstrap the OCCO environment. After checkout just
simply execute ``vagrant up`` and the virtual machine (created by VirtualBox) should be
correctly set up on your machine.

One should work on an OCCO component in a virtualenv. The following shows how
to setup the ``api`` repo. By doing this the ``occo-`` commands will appear
and work correctly.

.. code:: bash

    cd my-occo-dir
    cd api

    # Use this convenience script
    ./reset-env.sh
    
    #
    # This will print the path of the virtualenv; e.g.:
    source env/occo-api/bin/activate

To try the ``occo-`` commands, go to the Tutorial section of the Users' Guide
and follow the instructions. There you will find examples prepared for different
cloud backends and you can have proper configuration very fast. Users'
Guide can be found at the `Occopus Website`_. Alternatively, you can go to the 
``docs`` reporisory and find examples under the ``tutorial`` directory.

Virtualenvs should be placed in the ``env/`` directory, so they don't linger in
the working tree. ``git`` will ignore the contents of the ``env/`` directory so
virtualenvs will not be commited accidentally.

Testing
~~~~~~~

All components are developed using nosetests_. This means that in each
component there is an ``occo_test`` package containing test modules.

To test a package, one must first create a virtualenv and install the test
requirements in that virtualenv (see :ref:`cbe`).

When the test virtualenv is prepared, one must **always activate** it before
running the tests. The prompt changes after activating a virtualenv, so it's
easy to verify if it has been activated yet. Never *run* the ``activate``
script, one must always ``source`` it.

``nosetests`` must always be run from the top-level package directory. For
example, in case of the ``util`` package, it
must be run from e.g. ``my-occo-dir/util``. Running it from e.g.
``my-occo-dir/util/occo_test`` or anywhere else will not work.

RabbitMQ
^^^^^^^^

Some packages (Util, InfoBroker, InfraProcessor) need a message queue for some
of their tests.

In this case, a RabbitMQ server is needed to be set up. The access parameters
to the message queue are defined in various ``yaml`` files in the ``occo_test``
directory. Usually the hostname needs to be tweaked.

If needed, the RabbitMQ server can generally be configured using the following
commands (on the RabbitMQ server, as ``root`` ofcourse).

.. code:: bash

    rabbitmqctl add_vhost test
    rabbitmqctl add_user test test      # user: test, pass: test
    rabbitmqctl set_permissions -p test test .\* .\* .\*

.. todo:: This needs to be sanitized. Now that we have ``!yaml_import``, these
    access parameters can be extracted from the main configuration file, so
    they're not commited to the repository.

Packaging and deployment
------------------------

OCCO is split into several Python packages. The packages can be made available
on the LPDS internal PyPI server (or *package index*) as `Python wheels`_.

The **internal PyPI server** at the time of writing is on
``c155-10.localcloud``. It is accessible through an Apache proxy using the
``pip.lpds.sztaki.hu`` hostname.

Pip can use the following switches to use this package index:

.. code:: bash

    pip --trusted-host pip.lpds.sztaki.hu --find-links http://pip.lpds.sztaki.hu/packages --no-index

The packages must be **versioned** according to the `Semantic Versioning`_
standard.

Development should be done using locally checked out OCCO packages instead of
using package dependencies. The ``requirements_test.txt`` files rely on local
dependencies (``pip install -e ...``) to encourage this. This is to avoid
uploading too many useless package versions to the package index.

In each repository there is a ``package.sh`` which generates the wheels to be
published. ``upload.sh`` will upload the output package to ``c155-10``,
provided the uploader has root access to it.


.. _Python wheels: http://pythonwheels.com/
.. _Semantic Versioning: http://semver.org/

Managing the internal PyPI server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All dependencies can be found in this index. *Future dependencies* can be added
to the index thus:

.. code:: bash

    ssh -lroot c155-10.localcloud

    cd /opt/pypi-server/packages/

    pip wheel pymongo==2.8        # For example

This will download the new dependency from the community servers and installs
(caches) it on the internal PyPI server. Locally mirroring and maintaining all
used packages in an organization is a common practive anyway.

Dependency Manifests
~~~~~~~~~~~~~~~~~~~~

There are three dependency manifests to be maintained in each package.

    ``setup.py``

        Used by ``pip``, this module contains package information, including
        dependencies.

        The dependencies declared here are abstract (versionless) dependencies,
        declaring only the *relations* among packages.

    ``requirements.txt``

        Used for deployment, this text contains the *real dependencies* of the
        package, including version constraints.

        This file will be used by the users of OCCO, so it must contain package
        names as references and no source information (cf.
        ``requirements_test.txt``).
       
        This file should contain strict kinds of version specifications (``==``
        or possibly ``~>``), specifying the dependencies against which the
        package has been tested and verified.

    ``requirements_test.txt``

        This file specifies the packages needed to *test* the package. This includes
        nosetests_, and the current package itself (as a modifiable reference:
        ``-e .``).

        Unlike ``requirements.txt``, this file references other OCCO packages
        as local, modifiable repositories (e.g. ``-e ../util``). This helps the
        coding-testing cycle as modifications to other packages will be
        immediately "visible", without reinstallation.

        This file contains the source of the packages (LPDS internal PyPI
        server) hard-coded.

        This file must contain ``==`` type version specifications so the
        testing results are deterministic and reliable.

Creating Packages
~~~~~~~~~~~~~~~~~

The packages can be generated with the ``package.sh`` script in each package's
directory. This script creates and prepares an empty virtualenv and uses ``pip
wheel`` to generate wheels. While building the new wheel, it gathers all its
dependencies too, so the resulting ``wheelhouse`` directory will be a
self-contained set of packages that can be vendored. This script relies on
the internal PyPI server to gather the dependencies.

Vendoring Packages
~~~~~~~~~~~~~~~~~~

The generated wheel packages can be uploaded to the internal PyPI server using
the ``upload.sh`` script in each package's directory. It uploads everything
found in the ``wheelhouse`` directory generated by ``package.sh``. This is
redundant, as the dependencies already exist on the server, but this makes the
upload script dead simple.

When a package is uploaded, its version should be bumped unless it is otherwise
justified.

.. _pkgs:

Packages (in *a* topological order)
-----------------------------------

This is one possible topological ordering of the packages; i.e., they can be
built/tested/deployed in this order.

Only interdependencies are annotated here, dependencies on external packages
are omitted.

.. table:: **OCCO-Util**

    ===========  ===========================================================
    Depends      --
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/util
    Description  | Generic utility functions, configuration, communication,
                 | etc. See: :mod:`occo.util`.
    Testing      | The virtualenv must be bootstrapped by executing
                 | ``occo_test/bootstrap_tests.sh``.
    ===========  ===========================================================

.. table:: **OCCO-Compiler**

    ===========  ===========================================================
    Depends      OCCO-Util
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/compiler
    Description  | Compiler module for OCCO. See: :mod:`occo.compiler`.
    ===========  ===========================================================

.. table:: **OCCO-InfoBroker**

    ===========  ===========================================================
    Depends      OCCO-Util
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/info-broker
    Description  | Information broker for the OCCO system.
                 | See: :mod:`occo.infobroker`.
    ===========  ===========================================================

.. table:: **OCCO-Enactor**

    ===========  ===========================================================
    Depends      OCCO-Util, OCCO-Compiler, OCCO-InfoBroker
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/enactor
    Description  | Active component of the OCCO infrastructure maintenance
                 | system. See: :mod:`occo.enactor`.
    ===========  ===========================================================

.. table:: **OCCO-InfraProcessor**

    ===========  =========================================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/infrastructure-processor
    Description  | Central processor and synchronizer of the OCCO system. See:
                 | :mod:`occo.infraprocessor`.
    ===========  =========================================================================

.. table:: **OCCO-CloudHandler**

    ===========  ==============================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/cloud-handler
    Description  | Backend component of the OCCO system, responsible for
                 | handling specific kinds of clouds. This includes the
                 | generic plugin system, a dummy cloud handler for testing,
                 | and an EC2 ``boto`` cloud handler backend. See
                 | :mod:`occo.cloudhandler`.
    ===========  ==============================================================

.. table:: **OCCO-ServiceComposer**

    ===========  =================================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/service-composer
    Description  | Responsible for provisioning, setting up, configuring, etc.
                 | the nodes instantiated by the cloud handler.
    ===========  =================================================================

.. table:: **OCCO-API**

    ===========  =============================================================
    Depends      all OCCO packages
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/occo-api
    Description  | This package combines the primitives provided by other occo
                 | packages into higher level services and features. This
                 | package is intended to be the top-level package of the OCCO
                 | system upon which use-cases, user interfaces can be built.
    ===========  =============================================================

.. table:: **OCCO-Demo**

    ===========  ===============================================================
    Depends      all OCCO packages
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/occo-demo
    Description  | This package contains code that glues the packages of OCCO
                 | together into working example application. It is not intended
                 | to be released.
                 |
                 | This package can be used for experimenting, developing
                 | prototype code, integrating components, integration testing,
                 | demonstrating features, etc.
    ===========  ===============================================================

Continuous integration
----------------------

Continuous unit- and integration testing are to be set up on http://jenkins.lpds.sztaki.hu

Jenkins uses the ``c155-16.localcloud`` host as a slave for performing OCCO
tasks, using the ``jenkins`` user. 

The user ``jenkins@c155-16.localcloud`` has its own private ssh key in
``~/.ssh/``. This key is used for ssh connections outward this host, including
towards ``gitlab``. On ``gitlab``, the deploy key ``jenkins@c153-33`` (sic!) is
(or, at least, should be) enabled for all repositories used by Jenkins.

Documentation
-------------

The documentation you are reading is developed in the ``docs`` repository:

https://gitlab.lpds.sztaki.hu/cloud-orchestrator/docs

The documentation is developed using Sphinx_. Most of the documentation can be
found in the code; part of it is in the ``docs`` repository as
reStructuredText.

The ``docs`` repository contains a ``sphinx/`` directory, which contains a
`README.txt`_. This README contains step-by-step instructions on how to start
working on the documentation. The instructions in ``README.txt`` can be
copy-pasted in the shell, and they should work flawlessly. (Naturally, if you
have cloned all repositories already as described in :ref:`cbe`, you must omit
that part of the instructions.)

.. _README.txt: https://gitlab.lpds.sztaki.hu/cloud-orchestrator/docs/blob/master/sphinx/README.txt

Hint: As Sphinx ``import``\ s the Python packages, we need to make this
deployment clean: so it uses virtualenv too.

After preparing the ``docs`` environment, you can make the html documentation:

.. code:: bash

    make html

    ls build/html   # The result is here; it can be published in any way necessary

Documentation parameters
~~~~~~~~~~~~~~~~~~~~~~~~

Rendering the documentation can be configured and parameterized through the
Sphinx configuration file: ``source/conf.py``.

As this file is a dynamic module, it can be used to gather configuration
parameters dynamically (e.g.: environment variables). The current ``conf.py``
uses the following environment variables.

A string parsed as ``bool`` is considered to be :data:`True` if and only if it
starts with ``'t'``, ``'y'``, or ``'1'`` (``true``, ``yes``, ``1``; case-\
*in*\ sensitive).


    API_DOC

        If ``True``, parts of the documentation intended for OCCO developers
        are left out from the final document (e.g.: some warnings, todos, and
        this section altogether).

Example
~~~~~~~

.. code:: bash

    API_DOC=YES make html

.. _metadocs:

Sphinx plugin to autodoc InfoBroker keys
----------------------------------------

InfoBroker keys are automatically documented, and collated in the
:ref:`InfoBroker key index <ibkeyindex>` using a custom Sphinx extension.

.. warning:: Sphinx only compiles files it sees modified. So if the
    documentation of an InfoBroker key changes, or a key is added/removed, the
    change will only become visible if the file
    ``(docs repo)/sphinx/sources/ibkeys.rst`` is touched before making the
    documentation.

Info Broker Keys
~~~~~~~~~~~~~~~~

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

