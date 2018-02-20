****
pipw
****

.. image:: https://circleci.com/gh/danielzk/pipw/tree/master.svg?style=shield
    :target: https://circleci.com/gh/danielzk/pipw/tree/master
.. image:: https://img.shields.io/pypi/v/pipw.svg
    :target: https://pypi.python.org/pypi/pipw/
.. image:: https://img.shields.io/pypi/pyversions/pipw.svg
    :target: https://pypi.python.org/pypi/pipw/
.. image:: https://img.shields.io/codecov/c/github/danielzk/pipw/master.svg
    :target: https://codecov.io/gh/danielzk/pipw/branch/master

A wrapper for pip to save packages in requirements files similar to npm.

Installing
==========

.. code-block::

  $ pip install pipw

You can also pass an option to replace the pip command:

.. code-block::

  $ pip install pipw --install-option="--override-pip"

If you want to recover the pip command, you just have to reinstall pip. For
example:

.. code-block::

  $ pip uninstall pip
  $ easy_install pip

Usage
==========

TODO: add envs

.. code-block::

  pipw (install|uninstall) [-e] <package>... [options]

Options:

.. code-block::

  -s, --save           Save packages to the requirements file. This is default
                       unless --no-save. Packages are saved in
                       requirements.txt unless a custom configuration is used.
  -n, --no-save        Prevent save packages to the requirements file.
  -c, --config <path>  Pass a custom config file. By default it looks for a
                       .pipwrc file in the directory where the command is
                       executed.
  --help               Show this message and exit.

All pip commands and options are still available.

Config file
-----------

You can create a :code:`.pipwrc` file to use a custom configuration, or pass a
custom file with the :code:`--config` option.

Example of a config file:

.. code-block:: yaml

  requirements: requirements.txt
  specifier: ~=

Tests
=====

Tests are in :code:`tests/`. To run the tests use one of these commands:

.. code-block:: bash

  $ make tests
  $ make wip-tests
  $ make review-tests

You can also pass the environment. For example:

.. code-block:: bash

  $ make tests env=py35

Authors
=======

* **Daniel Ramos**
