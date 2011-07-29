``ezjail-remote`` is a 'remote control' and convenience wrapper for the ``ezjail-admin`` command of the most excellent `ezjail <http://erdgeist.org/arts/software/ezjail/>`_ tool (which in turn is itself a convenience wrapper for `jails <http://www.freebsd.org/doc/en_US.ISO8859-1/books/handbook/jails.html>`_, `FreeBSD <http://www.freebsd.org>`_'s leight-weight virtualization solution).

Its main features are:

 * more sophisticated support for flavours, i.e. interactive configuration and/or templating as opposed to ezjail's hardcoded flavours
 * you can ssh into jails created by ``ezjail-remote`` immediately upon creation (no more manual mucking about with sshd config or uploading your public key!)
 * unlike ``ezjail-admin``, ``ezjail-remote`` is not invoked on the jail host, but on your local machine.

Usage
=====

ezjail-remote uses the `fabric <http://docs.fabfile.org>`_ library to remotely run its tasks. Basically it provides a so-called *fabfile* that contains all of the commands of ``ezjail-admin`` (version 3.1 as of this writing).

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
