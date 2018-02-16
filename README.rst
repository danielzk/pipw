****
pipw
****

A wrapper for pip to save packages in requirements files similar to npm.

You can use it in the same way you use pip since this is just a wrapper.

Installing
==========

.. code-block::

  $ pip install pipw

You can also pass an option to overwrite the pip command instead of using
`pipw`:

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

  pipw (install|uninstall) <package>... [options]

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

TODO: add tox

Tests are in :code:`tests/`. To run the tests use one of these commands:

.. code-block:: bash

  $ make tests
  $ make wip-tests
  $ make review-tests

Authors
=======

* **Daniel Ramos**
