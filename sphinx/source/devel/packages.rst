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

.. important::

   We primarily support **Ubuntu** operating system. The following instruction steps were tested on **Ubuntu 18.04** version.

The OCCO packages are intended to be used in ``virtualenv`` under all
circumstances. This implies that:

There are only a few system-wide packages needed:

.. code:: bash
  
   sudo apt install -y python3-pip
   sudo apt install -y virtualenv
   sudo apt install -y redis-server
   sudo apt install -y libssl-dev
     
Git submodules can be used to clone and manage all repositories at once:

.. code:: bash

   git clone https://github.com/occopus/master.git github-occo --recursive
   cd github-occo
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

    cd github-occo
    cd api
    ./reset-env.sh
    source env/occo/bin/activate

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

    ssh ubuntu@192.168.155.11

    cd /opt/packages/

    pip download pymongo==2.8        # For example

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
    Repository   https://github.com/occopus/util.git
    Description  | Generic utility functions, configuration, communication,
                 | etc. See: :mod:`occo.util`.
    Testing      | The virtualenv must be bootstrapped by executing
                 | ``occo_test/bootstrap_tests.sh``.
    ===========  ===========================================================

.. table:: **OCCO-Compiler**

    ===========  ===========================================================
    Depends      OCCO-Util
    Repository   https://github.com/occopus/compiler.git
    Description  | Compiler module for OCCO. See: :mod:`occo.compiler`.
    ===========  ===========================================================

.. table:: **OCCO-InfoBroker**

    ===========  ===========================================================
    Depends      OCCO-Util
    Repository   https://github.com/occopus/info-broker.git
    Description  | Information broker for the OCCO system.
                 | See: :mod:`occo.infobroker`.
    ===========  ===========================================================

.. table:: **OCCO-Enactor**

    ===========  ===========================================================
    Depends      OCCO-Util, OCCO-Compiler, OCCO-InfoBroker
    Repository   https://github.com/occopus/enactor.git
    Description  | Active component of the OCCO infrastructure maintenance
                 | system. See: :mod:`occo.enactor`.
    ===========  ===========================================================

.. table:: **OCCO-InfraProcessor**

    ===========  =========================================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://github.com/occopus/infra-processor.git
    Description  | Central processor and synchronizer of the OCCO system. See:
                 | :mod:`occo.infraprocessor`.
    ===========  =========================================================================

.. table:: **OCCO-ResourceHandler**

    ===========  ==============================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://github.com/occopus/resource-handler.git
    Description  | Backend component of the OCCO system, responsible for
                 | handling specific kinds of clouds. This includes the
                 | generic plugin system, a dummy cloud handler for testing,
                 | and an EC2 ``boto`` cloud handler backend. See
                 | :mod:`occo.cloudhandler`.
    ===========  ==============================================================

.. table:: **OCCO-ConfigManager**

    ===========  =================================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://github.com/occopus/config-manager.git
    Description  | Responsible for provisioning, setting up, configuring, etc.
                 | the nodes instantiated by the cloud handler.
    ===========  =================================================================

.. table:: **OCCO-API**

    ===========  =============================================================
    Depends      all OCCO packages
    Repository   https://github.com/occopus/api.git
    Description  | This package combines the primitives provided by other occo
                 | packages into higher level services and features. This
                 | package is intended to be the top-level package of the Occopus
                 | system upon which use-cases, user interfaces can be built.
    ===========  =============================================================

Continuous integration
----------------------

Continuous unit- and integration testing are to be set up on http://jenkins.lpds.sztaki.hu

Jenkins uses the ``c155-16.localcloud`` host as a slave for performing OCCO
tasks, using the ``jenkins`` user. 

The user ``jenkins@c155-16.localcloud`` has its own private ssh key in
``~/.ssh/``. This key is used for ssh connections outward this host. 

Documentation
-------------

The documentation you are reading is developed in the ``docs`` repository:

https://github.com/occopus/docs.git

The documentation is developed using Sphinx_. Most of the documentation can be
found in the code; part of it is in the ``docs`` repository as
reStructuredText.

The ``docs`` repository contains a ``sphinx/`` directory, which contains a
`README.txt`_. This README contains step-by-step instructions on how to start
working on the documentation. The instructions in ``README.txt`` can be
copy-pasted in the shell, and they should work flawlessly. (Naturally, if you
have cloned all repositories already as described in :ref:`cbe`, you must omit
that part of the instructions.)

.. _README.txt: https://github.com/occopus/docs/blob/devel/sphinx/README.txt

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

