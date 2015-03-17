.. _packages:

Developer information for OCCO
==============================

.. _nosetests: https://nose.readthedocs.org
.. _virtualenv site: https://virtualenv.pypa.io
.. _Sphinx: http://sphinx-doc.org/

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
        
         * ``virtualenv`` version ``12.0.7`` or later. One can use any one of
           these methods:

            * ``sudo apt-get install python-virtualenv``
            * ``sudo easy_install virtualenv``
            * ``sudo pip install virtualenv``
         * git
         * Python 2.7

    #. All packages must declare all of their dependencies explicitly, without
       relying on implicit dependencies thought to be ubiquitous (e.g.
       argparse). (Because virtualenv-s are almost empty by default, containing
       only ``python`` and ``pip``.)

Currently, the simplest way to start working on OCCO is to clone all
repositories using the following script:

.. code:: bash

    mkdir my-occo-dir
    cd my-occo-dir

    REPOS='util compiler info-broker enactor infrastructure-processor cloud-handler service-composer occo-demo occo-api docs'

    for REPO in $REPOS; do
        git clone git@gitlab.lpds.sztaki.hu:cloud-orchestrator/$REPO.git
    done

Most scripts included in these components rely in this exact directory
structure (especially testing and documentation dependencies).

It would be nice to have a Vagrantfile or a prepared VM template to bootstrap
an OCCO environment; but right now we have to settle with this.

One should work on an OCCO component in a virtualenv. For example, to start
working on the ``util`` package:

.. code:: bash

    cd my-occo-dir
    
    cd util
    virtualenv env/util-dev                             # If does not exist yet
    source env/util-dev/bin/activate                    # Always after opening a new shell
    pip install --no-deps -r requirements_test.txt      # One time, after creating the virtualenv

    nosetests                                           # Optional anytime; Run all tests

    workworkwork

Testing
~~~~~~~

All components are developed using nosetests_. This means that in each
component there is an ``occo_test`` package containing test modules.

To test a package, one must first create a virtualenv and install the test
requirements in that virtualenv (see :ref:`cbe`).

When the test virtualenv is prepared, one must always activate it before
running ``nosetests``.

The peculiarity of ``nosetests`` is that it must always be run from the
top-level package directory. For example, in case of the ``util`` package, it
must be run from e.g. ``my-occo-dir/util``. Running it from e.g.
``my-occo-dir/util/occo_test`` (**common mistake**) or anywhere else will not
work.



Packaging and deployment
------------------------

OCCO is split into several Python packages. The packages can be made available
on the LPDS internal PyPI server (or *package index*) as `Python wheels`_.

The **internal PyPI server** at the time of writing is on
``c153-86.localcloud``.

The packages must be **versioned** according to the `Semantic Versioning`_
standard.

Development should be done using locally checked out OCCO packages instead of
using package dependencies. The ``requirements_test.txt`` files rely on local
dependencies (``pip install -e ...``) to encourage this. This is to avoid
uploading too many useless package versions to the package index.

.. _Python wheels: http://pythonwheels.com/
.. _Semantic Versioning: http://semver.org/

Managing the internal PyPI server
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The internal PyPI server must be bootstrapped if and when a **new external
dependency** is added to any of the OCCO packages. This means that the new
dependency must be installed there, so later phases of packaging can rely on
it. This is a simple task:

  - Login to the internal PyPI server as ``root``
  - ``cd /opt/pypi-server/packages/``
  - ``pip wheel [[new_dependency_name, and possibly version specification]]``

This will download the new dependency from the community servers and installs
(caches) it on the internal PyPI server.

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

    ===========  ===========================================================
    Depends      OCCO-Uti, OCCO-InfoBrokerl
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/infrastructure-processor
    Description  | Central processor and synchronizer of the OCCO system. See:
                 | :mod:`occo.infraprocessor`.
    ===========  ===========================================================

.. table:: **OCCO-CloudHandler**

    ===========  ===========================================================
    Depends      OCCO-Uti, OCCO-InfoBrokerl
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/cloud-handler
    Description  | Backend component of the OCCO system, responsible for
                 | handling specific kinds of clouds. This includes the
                 | generic plugin system, a dummy cloud handler for testing,
                 | and an EC2 ``boto`` cloud handler backend. See
                 | :mod:`occo.cloudhandler`.
    ===========  ===========================================================

.. table:: **OCCO-ServiceComposer**

    ===========  ===========================================================
    Note         *Under preliminary development; not integrated with other components yet.*
    Depends      OCCO-Util, OCCO-InfoBroker
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/service-composer
    Description  | Responsible for provisioning, setting up, configuring, etc.
                 | the nodes instantiated by the cloud handler.
    ===========  ===========================================================

.. table:: **OCCO-API**

    ===========  ===========================================================
    Note         *Under preliminary development; not integrated with other components yet.*
    Depends      all OCCO packages
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/occo-api
    Description  | This package combines the primitives provided by other occo
                 | packages into higher level services and features. This
                 | package is intended to be the top-level package of the OCCO
                 | system upon which use-cases, user interfaces can be built.
    ===========  ===========================================================

.. table:: **OCCO-Demo**

    ===========  ===========================================================
    Depends      all OCCO packages
    Repository   https://gitlab.lpds.sztaki.hu/cloud-orchestrator/occo-demo
    Description  | This package contains code that glues the packages of OCCO
                 | together. It is not intended to be released.
                 |
                 | This package can be used for experimenting, developing
                 | prototype code, integrating components, integration testing,
                 | demonstrating features, etc.
    ===========  ===========================================================

Documentation
=============

The documentation you are reading is developed in the ``docs`` repository:

https://gitlab.lpds.sztaki.hu/cloud-orchestrator/docs

The documentation is developed using Sphinx_. Most of the documentation can be
found in the code; part of it is in the ``docs`` repository as
reStructuredText.

The ``docs`` repository contains ``sphinx/`` directory, which contains a
``README.txt``. This README contains step-by-step instructions on how to start
working on the documentation. The instructions in ``README.txt`` can be
copy-pasted in the shell, and they should work flawlessly. (Naturally, if you
have cloned all repositories already as described in :ref:`cbe`, you must omit
that part of the instructions.)

Hint: As Sphinx ``import``\ s the Python packages, we need to make this
deployment clean: so it uses virtualenv too.

After preparing the ``docs`` environment, you can make the html documentation:

.. code:: bash

    make html

    ls build/html   # The result is here; it can be published in any way necessary

Continuous integration
======================

Continuous unit- and integration testing are to be set up on http://jenkins.lpds.sztaki.hu

Unit testing is partly done at the time of writing.
