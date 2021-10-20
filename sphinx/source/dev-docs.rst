
.. _dev-docs:

Develop documentation
------------------------

This guide aims to help you get familiar with the Occopus documentation part.

.. _create-docs-env:

Creating documentation environment locally
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set up a documentation environment you need to have a ``Python3`` installation with installed ``Spinx`` and ``sphinx_rtd_theme`` package.

The documentation tested with the following versions:

    * Sphinx - ``3.0.3``
    * sphinx_rtd_theme - ``0.4.3``


To create a local documentation environment just follow the steps (Debian-based OS):

.. code:: bash

    sudo apt update && sudo apt install -y python3-pip virtualenv
    virtualenv -p python3 ./venv/docs
    source venv/docs/bin/activate
    git clone https://github.com/occopus/docs.git -b devel
    pip install -r docs/sphinx/requirements.txt
    cd docs/sphinx/
    make html


.. note::
    It is recommended to use virtual environment however you can continue without it.

Now you can easily build your own documentation with ``make html`` command under ``docs/sphinx/`` path. After the process finished, you can find the built documentation under ``docs/sphinx/build``.

.. _visualize-docs:

Visualize local build
~~~~~~~~~~~~~~~~~~~~~

For **testing purposes** you can install nginx and host your documentation. The following steps will help you to do that:

.. code:: bash

    sudo apt update && sudo apt install -y nginx
    sudo sed -i "s/^        root/        root \/home\/ubuntu\/docs\/sphinx\/build\/html\;/g" \
    /etc/nginx/sites-available/default
    # the sed part could be different in different OS. If it does not work, just replace the root
    # line with your docs location
    sudo service nginx restart

After these steps, you can look at the documentation under: ``http://[Your_IP_Address]/``

.. danger::
    Nginx config is **not** a valid production ready config! Use **only** for **testing** purposes!
    If you are able to do that do not expose it to the public (use local network if it is possible).

Helper scripts
~~~~~~~~~~~~~~

Under the documentation repository, there is helperScripts folder with two different helper scripts.
It provides quick automation of different tasks.

createTarFileFromTutorials.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script creates a tar.gz file from every directory from ``docs/tutorials``. It is important to run this
script when you modify the description in the tutorials folder. The tar.gz file requires to make tutorials downloadable through
hosted documentation (Read the Docs) via raw GitHub URL.

updateAbsoluteGithubLinksToChangeBranch.sh
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This script aids to help change the GitHub branch absolute path easily through a semi-automated way.
The script requires two arguments. First argument is the **current** branch and the second argument is the **target** branch.

The script looks through the following path, and modify the branch if needed:

* ``/sphinx/source/*.rst``
* ``/tutorials/``

Usually, there are two common usages but you can modify as you wish:

This way the script change every ``master`` branch reference to the ``devel`` branch.

.. code:: bash

    $ ./updateAbsoluteGithubLinksToChangeBranch.sh master devel

The other way does the opposite. The script change every ``devel`` branch reference to the ``master`` branch.

.. code:: bash

    $ ./updateAbsoluteGithubLinksToChangeBranch.sh devel master


Read the Docs build
~~~~~~~~~~~~~~~~~~~

Every tag creates a new version for the Occopus documentation site. Occopus documentation is
hosted by Read the Docs (RTD) at the URL: https://occopus.readthedocs.io.

The ``master`` branch defines the lastest tag in RTD which is considered as the
stable version of the documentation. Each releases of the master branch is compiled and shown by RTD as versions.

Actual version of the ``devel`` branch is also continuesly refreshed by RTD and shown under a hidden (/devel) URL. Optionally,
it can be built privately on your local machine as described in sections :ref:`create-docs-env` and :ref:`visualize-docs`.

If there is a new tag or commit in master or devel branch in Occopus Docs repository RTD will rebuild the whole
documentation. After a while the documentation will be available with the changes through the documentation URL.