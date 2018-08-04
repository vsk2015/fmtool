Project Overview
================

This tool provides a mechanism to test and validate Lumina Flow Manager application with OVS and Noviflow switches. It also includes obtaining eline/etree/flows/groups stats and summary information, as well as the ability to perform actions such as deleting flows and groups.

Directory Structure
~~~~~~~~~~~~~~~~~~~

.. literalinclude:: dir_structure.txt


Installation
~~~~~~~~~~~~

Clone the project from the Telstra SEN Bitbucket repository.

::

$ cd flow-manager-tools
$ sudo python setup.py install

Usage
~~~~~

**fmcheck** will be the command after installation. This is to allow users to test `fmcheck` and `fmcheck` side by side. Eventually fmcheck will become fmcheck.


Dependencies
~~~~~~~~~~~~

The following dependencies are installed with the installation.

- pexpect
- pyyaml
- requests
- coloredlogs

Documentation
~~~~~~~~~~~~~

To create the documentation you need to do the following:

::

$ cd flow-manager-tools/docs
$ make html

The generated files and web page will now be located in **flow-manager-tools/docs/_build**.
