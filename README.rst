``ezjail-remote`` is a 'remote control' and convenience wrapper for the ``ezjail-admin`` command of the most excellent `ezjail <http://erdgeist.org/arts/software/ezjail/>`_ tool (which in turn is itself a convenience wrapper for `jails <http://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/jails.html>`_, `FreeBSD <http://www.freebsd.org>`_'s leight-weight virtualization solution).

Its main features are:

 * more sophisticated support for flavours, i.e. interactive configuration and/or templating as opposed to ezjail's hardcoded flavours
 * you can ssh into jails created by ``ezjail-remote`` immediately upon creation (no more manual mucking about with sshd config or uploading your public key!)
 * unlike ``ezjail-admin``, ``ezjail-remote`` is not installed on the jail host, but on your local machine. This means *it doesn't introduce any further dependencies on the jail host whatsoever* (ezjail itself purposefully limits itself to ``sh``).

..note: In general ezjail-remote tries to keep up with ezjail development, so unless stated otherwise, it requires (and by default also installs) the latest version of ezjail (version 3.2.2 as of this writing).

Usage
=====

ezjail-remote uses the `fabric <http://docs.fabfile.org>`_ library to remotely run its tasks. Basically it provides a so-called *fabfile* that contains all of the commands of ``ezjail-admin``.

This means that its usage differs slightly from that of ``ezjail-admin``. In particular, you provide the hostname of the jail server via the ``-H`` switch and the parameters for the command (such as the name of the jail etc) separated with a colon, like so::

  ezjail-remote -H host(s) <COMMAND>:param1,param2,param3

or::

  ezjail-remote -H host(s) <COMMAND>:param1=foo,param3=bar

See the `full documentation of what fabric has to offer here <http://docs.fabfile.org/en/1.2.0/usage/fab.html#command-line-options>`_.

In particualar, you can...

 * run ``ezjail-remote --help`` to see a list of the available *options*
 * run ``ezjail-remote -l`` to see a list of the available *commands*
 * run ``ezjail-remote -d COMMAND`` to see a detailed description of a command

As a side effect of using fabric, you can run ezjail-admin commands against multiple jailhosts at the same time.

Bootstrapping
=============

ezjail-remote doesn't only make it easy to create and manage jails, it also helps you set up a jailhost environment from scratch. This is done with the ``bootstrap`` and ``install`` commands.

To successfully run the bootstrap command the following requirements need to be met on the host:

 * sshd is up and running
 * ssh login for root is (temporarily) enabled
 * currently we also require an internet connection (to install ezjail) but this will eventually be replaced with uploading a copy of ezjail.

For example (logged in as root on the console)::

  echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
  echo 'ifconfig_em0=DHCP' >> /etc/rc.conf
  passwd # give yourself a TEMP_PASSWORD
  dhclient em0 # note the IP_ADDR you get
  /etc/rc.d/sshd onestart


Now you can run the bootstrap command using the temporary password you gave yourself::

  ezjail-remote -H IP_ADDR bootstrap

This 

 * disables root login
 * permanently enables SSH for the jail host (and limits it to the primary IP address)
 * creates an admin user with your username and public SSH key

..note: Before installing ezjail with the ``install`` command you may want to set up additional things, such as ZFS pools, network interface aliases, etc.

To install ezjail you can use the ``install`` command, which either installs it from the ports or from CVS (for the brave)::

  ezjail-remote -H IP_ADDR install

If you want to use a CVS snapshot::

  ezjail-remote -H IP_ADDR install:source=cvs

If you want to use ZFS (and you should!) supply the pool it should use via the jailzfs parameter::

  ezjail-remote -H IP_ADDR install:jailzfs='jails/ezjail'


Commands
========

In its simplest form, ezjail remote offers the exact same commands as ezjail-admin, namely ``[archive|config|console|create|delete|install|list|restore|start|stop|update]``. In addition to that it provides enhanced versions of ``create`` and ``destroy`` (the latter a more thorough variant of the ``delete`` command.)

create
------

creates a new jail instance on the given host, creates an admin user with sudo privileges and enables ssh access via public key.

after setting up the jail it attempts to execute a method named ``setup`` from ``ezjailremote.flavours.<name-of-flavour>``, passing on all parameters, including any additional, arbitrary keyword arguments.

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

ctype
  defaults to None and refers to the `-c` flag, meaning, you can set it to `simple`, `bde`, `eli` or `zfs`.


destroy
-------

stops, removes and deletes the given jail instance (but not before asking you one last time, explicitely). however, once you confirm, the jail is irrevocably *gone*.

parameters
**********

name
  name of the new jail, *required*

Installation
============

Simply use easy_install::

  easy_install ezjail-remote

Development
===========

To develop ezjail-remote itself, check out a copy of this repository and then::

  virtualenv . --no-site-package
  ./bin/python setup.py develop

TODO
====

 * document flavour development
 * use a base class for flavours
 * list them (with their docstr) with ezjail-remote list-flavours
 * allow chaining/nesting/stacking of flavours (i.e. always include basic)

Change history
==============

0.2.2 - Unreleased
------------------

 * Use ezjail version 3.2.2 feature to create ZFS jails by default
 * Make use and configuration of sshd in created jail optional
 * Various smaller bugfixes
 * officially out of alpha :)

0.2.1 - 2012-09-10
------------------

 * add support for creating ZFS (and other image based) jails

0.2 - 2012-09-07
----------------

 * split installation into ``bootstrap`` (which has proven itself useful outside of a ezjail setup) and ``install``
 * added support for ZFS
 * can install ezjail from CVS
 * added support for flavours outside the ezjail-remote package itself (using namespace packages for ezjailremote.flavours.\*)
 * added `start`, `stop` and `jls` commands.

0.1 - 2011-07-29
----------------

Initial release. Provides 'pass through' of all commands, as well as enhanced versions for ``create`` and ``destroy``.
