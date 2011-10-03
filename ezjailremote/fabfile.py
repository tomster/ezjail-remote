import sys
from os import path
from datetime import datetime

from fabric.api import sudo, put, env, run, settings, prompt, task, hide
from fabric.state import output
from fabric.contrib.files import upload_template


EZJAIL_JAILDIR = '/usr/jails'
EZJAIL_RC = '/usr/local/etc/rc.d/ezjail.sh'
EZJAIL_ADMIN = '/usr/local/bin/ezjail-admin'

env['shell'] = '/bin/sh -c'
output['running'] = False

@task
def install(install_ports=False):
    sudo("pkg_add -r ezjail")
    install_basejail = "%s install"
    if install_ports:
        install_basejail += " -P"
    sudo(install_basejail)


@task
def create(name,
    ip,
    admin=None,
    keyfile=None,
    flavour=u'basic',
    **kw):

    """<name>,<ip>(,<admin>,<keyfile>,flavour)

    Create a jail instance with the given name and IP address.
    Configures ssh access for the given admin user and ssh key.

    admin: defaults to the current user
    keyfile: defaults to ~/.ssh/identity.pub
    flavour: defaults to 'basic' and refers to a LOCAL flavour, NOT any on the host

    any additional keyword arguments are passed to the flavour
    """

    if admin is None:
        admin = env['local_user']

    if keyfile is None:
        keyfile = path.expanduser("~/.ssh/identity.pub")

    if not path.exists(keyfile):
        sys.exit("No such keyfile '%s'" % keyfile)

    print("name: %s, ip: %s, flavour: %s" % (name, ip, flavour))

    try:
        flavour_module = __import__('ezjailremote.flavours.%s' % flavour, globals(), locals(), ['setup'], -1)
    except ImportError:
        sys.exit("No such flavour '%s'" % flavour)
    local_flavour_path = path.abspath(path.dirname(flavour_module.__file__))

    with settings(warn_only=True):
        tmp_flavour = '%s-%s' % (flavour, datetime.now().strftime('%Y%m%d%H%M%s'))
        remote_flavour_path = path.join(EZJAIL_JAILDIR, 'flavours', tmp_flavour)
        sudo("mkdir %s" % remote_flavour_path)
        sudo("chown %s %s" % (env['user'], remote_flavour_path))
        put("%s/*" % local_flavour_path, remote_flavour_path)
        local_flavour_script = path.join(local_flavour_path, 'ezjail.flavour')
        if path.exists(local_flavour_script):
            upload_template(local_flavour_script,
                path.join(remote_flavour_path, 'ezjail.flavour'),
                context=locals(), backup=False)
        else:
            print "Warning! no ezjail.flavour found (expected one at %s)" % local_flavour_script

        # create the jail using the uploaded flavour
        create_jail = sudo("%s create -f %s %s %s" % (EZJAIL_ADMIN, tmp_flavour, name, ip))
        if create_jail.succeeded:
            jail_path = path.join(EZJAIL_JAILDIR, name)
            # copy resolv.conf from host
            sudo("cp /etc/resolv.conf %s" % path.join(jail_path, 'etc', 'resolv.conf'))
            # copy the key file into flavour
            ssh_config = path.join(jail_path, 'home', admin, '.ssh')
            sudo("mkdir -p %s" % ssh_config)
            remote_keyfile = path.join(ssh_config, 'authorized_keys')
            put(keyfile, remote_keyfile, use_sudo=True)
            sudo("chown -R %s %s" % (admin, ssh_config))
            # start up the jail:
            sudo("%s start %s" % (EZJAIL_RC, name))
            # perform any additional setup the flavour may provide
            if hasattr(flavour_module, 'setup'):
                flavour_module.setup(name, ip, admin, keyfile, **kw)
        sudo("rm -rf %s" % remote_flavour_path)


@task
def destroy(name):
    """<name>"""
    really = prompt('Are you ABSOLUTELY sure you want to destroy the jail %s?\n'
        'The jail will be stopped if running, deleted from ezjail and on the filesystem!!\n'
        'Type YES to continue:' % name)
    if really != 'YES':
        sys.exit("Glad I asked...!")
    sudo("%s stop %s" % (EZJAIL_RC, name))
    sudo("%s delete -w %s" % (EZJAIL_ADMIN, name))


@task(default=True, aliases=['archive', 'config', 'console', 'delete', 'install', 'list', 'restore', 'update', 'start', 'stop'])
def usage(*xargs, **kw):
    """(passed directly to ezjail-admin)"""
    command = env.get('command')
    if command == 'usage':
        command = '--help'
    args_string = ''
    for item in kw.items():
        args_string += '%s %s ' % item
    with hide('warnings', 'aborts'):
        sudo("%s %s %s %s" % (EZJAIL_ADMIN, command, args_string, ' '.join(xargs)))


@task
def jls():
    run("jls")
