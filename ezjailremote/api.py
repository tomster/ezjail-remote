import inspect
from os import path
from fabric import api as fab
from fabric.contrib.project import rsync_project
from fabfile import create, destroy



class BaseJail(object):
    """
        Represents a to-be-created or already existing jail instance.

        It provides three methods: create, configure and update which it expects to be run
        from a fabfile with a connection to the jail host.

        ``create`` and ``configure`` are expected to be run as-is, whereas ``extra_configure``
        (which is called by ``configure`` at the end) and ``update`` are expected to be overridden
        by any subclass.

    """

    name = ""
    ctype = 'zfs'
    sshd = False
    ip_addr = None
    fs_local_root = None
    fs_remote_root = None
    configurehasrun = False
    ports_to_install = []

    def __init__(self, **config):
        """
        Instantiate it with arbitrary parameters, but the following are mandatory:

        :param name: name of the jail
        :param: ip_addr: its IP address
        :param sshd: if True, an admin user will be created using the name and default ssh key of the user
            calling the fabfile and sshd will be configured and run inside the jail. Set this to False if
            you want to create a jail with a private IP which should not be accessible from outside the jailhost.
        :param ports_to_install: a list of strings denoting any ports that should be installed during ``configure``.
            The names are expected to be relative to ``/usr/ports``, i.e. ``lang/python``.
        :param fs_local_root: local path to a directory tree which will be uploaded to the root of the new jail during ``configure``.
            If None, a local path with the name of the jail relative to the location of the file containing the instance
            of thsi class is assumed.
            One use-case for this is to provide port configuration files in ``/var/db/ports/*/options`` which allows the ports
            installation to run without user-intervention.
        :param fs_remote_root: path to the jail, defaults to ``/usr/jails/NAMEOFJAIL``.
        :param ctype: passed as ``-type`` to ``ezjail-admin create``
        """
        for key, value in config.items():
            setattr(self, key, value)
        # if we didn't get an explict root, set a default:
        if self.fs_local_root is None:
            self.fs_local_root = '%s/' % path.join(path.abspath(path.dirname(inspect.getfile(self.__class__))), self.name)
        if self.fs_remote_root is None:
            self.fs_remote_root = '/usr/jails/%s' % self.name

    def create(self):
        create(self.name,
            self.ip_addr, ctype=self.ctype, sshd=self.sshd)

    def configure(self):
        # upload site root
        if path.exists(self.fs_local_root):
            fab.sudo('rm -rf /tmp/%s' % self.name)
            rsync_project('/tmp/%s/' % self.name, self.fs_local_root,
                extra_opts='--perms --executability -v --super')
            fab.sudo('rsync -rav /tmp/%s/ /usr/jails/%s/' % (self.name, self.name))
            fab.sudo('rm -rf /tmp/%s' % self.name)
        # install ports
        for port in self.ports_to_install:
            self.console('make -C /usr/ports/%s install' % port)
        self.extra_configure()
        self.configurehasrun = True

    def extra_configure(self):
        pass

    def update(self):
        pass

    def destroy(self):
        destroy(self.name)

    def console(self, command):
        """ execute the given command inside the jail by calling ezjail-admin console.
        This is particularly useful for jails w/o sshd and/or a public IP
        """
        fab.sudo('''ezjail-admin console -e "%s" %s''' % (command, self.name))
