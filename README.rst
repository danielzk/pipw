****
pipw
****

|build| |pipw| |python| |coverage| |license|

A wrapper for pip to save packages in requirements files similar to npm.

There are better alternatives to pip (like `Pipenv <https://github.com/pypa/pipenv>`_), but this was created for
those who want or need to continue using pip. For example, those who
collaborate in projects that use pip requirements files.

Installing
==========

.. code-block::

  $ pip install pipw

Usage
==========

.. code-block::

  pipw (install|uninstall) [-e] <package>... [options]

Options:

.. code-block::

  -s, --save           Save packages to the requirements file. This is default
                       unless --no-save. Packages are saved in
                       requirements.txt unless a custom configuration is used.
  -n, --no-save        Prevent save packages to the requirements file.
  --config <path>      Pass a custom config file. By default it looks for a
                       .pipwrc file in the directory where the command is
                       executed, or in the user's home directory.
  -m, --env <name>     Save in a environment previously declared in the config
                       file.
  --save-to <path>     Save to a custom file.
  --no-detect-version  Do not detect installed version, and save package
                       version only if the version is passed.
  --help               Show this message and exit.

All pip commands and options are still available.

Config file
-----------

You can create a :code:`.pipwrc` file to use a custom configuration. By default
it looks for the file in the directory where the command is executed, or in the
user's home directory. You can also pass a custom file to the :code:`--config`
option.

Example of a config file:

.. code-block:: yaml

  requirements: requirements.txt
  specifier: ~=
  detect_version: true
  envs:
      dev: requirements/dev.txt

Environments
------------

As you can see, you can set environment files in the configuration file:

.. code-block:: yaml

  requirements: requirements/prod.txt
  envs:
      dev: requirements/dev.txt
      test: requirements/test.txt

Use the `-m` (or `--env`) option to save the packages in an environment file:

.. code-block::

  $ pipw install pytest -m test

If no environment is passed, the value defined in `requirements` are used by
default. If this value is not defined, a `requirements.txt` file is used by
default. These files are created automatically if they do not exist.

The `uninstall` command will remove the package in all files, unless the `-m`
option is passed.

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

.. |build| image:: https://circleci.com/gh/danielzk/pipw/tree/master.svg?style=shield
    :target: https://circleci.com/gh/danielzk/pipw/tree/master
.. |pipw| image:: https://img.shields.io/pypi/v/pipw.svg
    :target: https://pypi.python.org/pypi/pipw/
.. |python| image:: https://img.shields.io/pypi/pyversions/pipw.svg
    :target: https://pypi.python.org/pypi/pipw/
.. |coverage| image:: https://img.shields.io/codecov/c/github/danielzk/pipw/master.svg
    :target: https://codecov.io/gh/danielzk/pipw/branch/master
.. |license| image:: https://img.shields.io/badge/License-MIT-blue.svg
    :target: https://opensource.org/licenses/MIT
