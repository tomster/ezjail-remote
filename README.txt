ezjail-remote is a fabric based wrapper around the ``ezjail-admin`` command offering better support for its flavours, notably parameters and interactive configuration.

it installs an executable named ``ezjail-remote`` with the following commands, each a wrapper for its identically named ``ezjail-admin`` counterpart.

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

hosts
  list of hosts

admin
  name of the admin user to create

keyfile
  public key for that admin user. if none is provided, a private key will be created and its public part installed.


create
------

creates a new jail instance on the given host. it uses the *ezjail-remote* flavor by default, which in turn allows us to perform further (even interactive) customizations that 'naked' ezjail flavors don't allow for.

parameters
**********

host
  name of the jailhost, *required*

name
  name of the new jail, *required*

IP
  the IP address, *required*

admin
  name of the admin user for the jail, defaults to ``admin``.

keyfile
  public key for that admin user. if none is provided, a private key will be created and its public part installed.

flavour
  *optional* the name of a registered flavour. Note that this explicitly does *not* correspond to any ezjail flavours on the jail host

Extending ezjail-remote
=======================

Of course, the real fun starts once you create more elaborate commands that can use the full power and flexibility of fabric. like ezjail, we call these *flavours*.

note: perhaps use ZCA to register flavours?
 