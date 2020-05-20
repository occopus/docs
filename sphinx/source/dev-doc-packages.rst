.. _packages:

.. _nosetests: https://nose.readthedocs.org
.. _virtualenv site: https://virtualenv.pypa.io
.. _Sphinx: http://sphinx-doc.org/
.. _Occopus Website: http://occopus.lpds.sztaki.hu

.. figure:: images/logo/occo_dev.png
    :align: left

*Always* use ``virtualenv`` for any kind of deployment (testing, building,
production, ... everything). This ensures there will be no dependency issues:
deployment collisions, missing dependencies in releases, etc. See the
`virtualenv site`_ for details.

|
|

Build environment
-----------------

.. _cbe:

.. important::

   We primarily support **Ubuntu** operating system. The following instruction steps were tested on **Ubuntu 18.04** version.

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

There is a Vagrantfile to bootstrap the Occopus environment. After checkout just
simply execute ``vagrant up`` and the virtual machine (created by VirtualBox) should be
correctly set up on your machine.

One should work on an Occopus component in a virtualenv. The following shows how
to setup the ``api`` repo. By doing this the ``occopus-`` commands will appear
and work correctly.

.. code:: bash

    cd github-occopus
    cd api
    ./reset-env.sh
    source env/occopus/bin/activate

To try the ``occopus-`` commands, go to the Tutorial section of the Users' Guide
and follow the instructions. There you will find examples prepared for different
cloud backends and you can have proper configuration very fast. Users'
Guide can be found at the `Occopus Website`_. Alternatively, you can go to the
``docs`` reporisory and find examples under the ``tutorial`` directory.

Virtualenvs should be placed in the ``env/`` directory, so they don't linger in
the working tree. ``git`` will ignore the contents of the ``env/`` directory so
virtualenvs will not be commited accidentally.


Packaging and deployment
------------------------

Occopus is split into several Python packages. The packages can be made available
on the LPDS internal PyPI server (or *package index*) as `Python wheels`_.

The **internal PyPI server** at the time of writing is on
``192.168.155.11``. It is accessible through an Apache proxy using the
``pip3.lpds.sztaki.hu`` hostname.

Pip can use the following switches to use this package index:

.. code:: bash

    pip --trusted-host pip3.lpds.sztaki.hu --find-links http://pip3.lpds.sztaki.hu/packages --no-index

The packages must be **versioned** according to the `Semantic Versioning`_
standard.

Development should be done using locally checked out Occopus packages instead of
using package dependencies. The ``requirements_test.txt`` files rely on local
dependencies (``pip install -e ...``) to encourage this. This is to avoid
uploading too many useless package versions to the package index.

In each repository there is a ``package.sh`` which generates the wheels to be
published. ``upload.sh`` will upload the output package to the ``pip3.lpds.sztaki.hu``,
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

        This file will be used by the users of Occopus, so it must contain package
        names as references and no source information (cf.
        ``requirements_test.txt``).

        This file should contain strict kinds of version specifications (``==``
        or possibly ``~>``), specifying the dependencies against which the
        package has been tested and verified.

    ``requirements_test.txt``

        This file specifies the packages needed to *test* the package. This includes
        nosetests_, and the current package itself (as a modifiable reference:
        ``-e .``).

        Unlike ``requirements.txt``, this file references other Occopus packages
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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
    Description  | Backend component of the OCCO system, responsible
                 | for handling specific kinds of resources. See
                 | :mod:`occo.resourcehandler`.
    ===========  ==============================================================

.. table:: **OCCO-ConfigManager**

    ===========  =================================================================
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://github.com/occopus/config-manager.git
    Description  | Responsible for provisioning, setting up, configuring, etc.
                 | the nodes instantiated by the resource handler.
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
