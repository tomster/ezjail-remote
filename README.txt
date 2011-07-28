ezjail-remote is a fabric based wrapper around the ``ezjail-admin`` command offering better support for its flavours, notably parameters and interactive configuration.

Usage
=====

./bin/ezjail-remote -H hosts <COMMAND>:param1,param2,param3

or

./bin/ezjail-remote -H hosts <COMMAND>:param1=foo,param3=bar


Commands
========

install
-------

bootstraps the host system. 

 * installs ezjail
 * creates an admin-user
 * tweaks the sshd config
 * installs the *ezjail-remote* flavor so that all further commands can be run via fabric

requires root login on the host (and ssh access, obviously)

parameters
**********

admin
  name of the admin user to create

keyfile
  public key for that admin user. if none is provided, a private key will be created and its public part installed.


create
------

creates a new jail instance on the given host, creates an admin user with sudo privileges and enables ssh access via public key.

parameters
**********

name
  name of the new jail, *required*

IP
  the IP address, *required*

admin
  name of the admin user for the jail, defaults to the current user. the user will be created and added to ``wheel`` (which in turn will be allowed to sudo without password).

keyfile
  public key to install for the admin user, defaults to ``~/.ssh/identity.pub``.

flavour
  the name of the local flavour, defaults to ``basic``.


Development
===========

  virtualenv . --no-site-package
  ./bin/python setup.py develop
