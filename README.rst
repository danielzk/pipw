****
pipw
****

Wrapper for pip to save packages in requirements files similar to npm.

Installing
==========

TODO: add setup tools

Usage
==========

TODO: add envs

.. code-block:: none

  pipw (install|uninstall) <package>... [options]

Options:

.. code-block:: none

  -s, --save           Save packages to the requirements file. This is default
                       unless --no-save. Packages are saved in
                       requirements.txt unless a custom configuration is used.
  -n, --no-save        Prevent save packages to the requirements file.
  -c, --config <path>  Pass a custom config file. By default it looks for a
                       .pipwrc file in the directory where the command is
                       executed.
  --help               Show this message and exit.

All pip commands are available while this is just a wrapper.

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

TODO: add tox

Tests are in :code:`tests/`. To run the tests use:

.. code-block:: bash

  $ pytest

Authors
=======

* **Daniel Ramos**
