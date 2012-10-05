This directory contains tested and working examples. You should be able to run them simply by providing a custom ``jails.conf`` for your host environment.

To get started, create a minimal version of ``jails.conf`` like so::

    [host]
    ip_addr = 192.168.91.128

Replace the value for ``ip_addr`` with that of your jail host. 

Bootstrapping
=============

Bootstrapping is an optional convenience command to setup the jail host to meet the requirements to install and run ezjail-remote.

The default bootstrap does the following:

 * creates and admin user and uploads his sshkey 
 * installs ``sudo`` and enables passwordless access for the admin user

In order to run bootstrap on a remote host, the following criteria must be met:

 * ``sshd`` is up and running on ``ip_addr``
 * ``RootLogin`` is enabled (in ``/etc/ssh/sshd_config``)

Then ``cd`` into the examples directory and::

    # ezjail-deploy bootstrap

If you already have remote sudo access (i.e. if your testing this locally) you can skip bootstrapping by running the ``install`` command directly::

    # ezjail-deploy install

Note: running ``bootstrap`` will always also run ``install`` for you.

Either way, you now should be able to ssh into the host and run ezjail-admin::

    # ssh 192.168.91.128
    [...]
    $ sudo ezjail-admin -v
    ezjail-admin v3.2
    Usage: ezjail-admin [archive|config|console|create|delete|install|list|restore|update] {params}


Deploying a jail
================

Now you're ready to deploy the first example. First, exit the ssh shell - from now on we're going to do everything remotely, afterall::

    $ exit

For this example we will install a simple forwardinf and caching nameserver using the excellent ``unbound`` daemon. To do so simply run::

    # ezjail-deploy init unbound

This will:

 * create a jail named ``unbound`` listening on the ip address of the jail host
 * install ``dns/unbound`` from ports
 * configure it to listen on the local network
 * enable it and start it up,

 If all went well, you now should be able to run queries against it::

    # dig @192.168.91.128 github.com


Nameserver Jail
---------------