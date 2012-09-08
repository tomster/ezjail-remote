import sys
from os import path
from datetime import datetime

from fabric.api import sudo, put, env, run, settings, prompt, task, hide, puts, show, warn, cd
from fabric.contrib.files import upload_template

from ezjailremote.utils import kwargs2commandline, jexec, get_flavour, is_ip

EZJAIL_JAILDIR = '/usr/jails'
EZJAIL_RC = '/usr/local/etc/rc.d/ezjail'
EZJAIL_ADMIN = '/usr/local/bin/ezjail-admin'

env['shell'] = '/bin/sh -c'
# output['output'] = False
# output['running'] = False


@task
def bootstrap(admin=None,
    keyfile=None,
    primary_ip=None):
    """ assuming we have ssh access as root sets up permanent ssh access, creates the admin user with
    ssh access and sudo privileges, then shuts out root login again.

    admin: username for the admin account, defaults to your local username
    keyfile: full path to your public SSH key, defaults to ~/.ssh/identity.pub
    primary_ip: the IP address for which to configure the jailhost, can be omitted if the host is given
        as an IP address with the -H parameter
    """
    # force user to root
    env['user'] = 'root'
    # check for admin user and key:
    if admin is None:
        admin = env['local_user']
    if keyfile is None:
        keyfile = path.expanduser("~/.ssh/identity.pub")
    if not path.exists(keyfile):
        sys.exit("No such keyfile '%s'" % keyfile)

    pkg_info = run("pkg_info")
    with settings(hide("everything"), warn_only=True):
        user_info = run("pw usershow %s" % admin)

    if primary_ip is None and is_ip.match(env['host']):
        primary_ip = env['host']

    if primary_ip is None:
        warn("No primary IP address specified!")
    else:
        run("grep -v ListenAddress /etc/ssh/sshd_config > /etc/ssh/sshd_config.tmp")
        run("echo 'ListenAddress %s' >> /etc/ssh/sshd_config.tmp" % primary_ip)
        run("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
        run("mv /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config")
    # prevent syslogd listening on any addresses (to avoid warnings at jail startup)
    run("echo syslogd_flags='-ss' >> /etc/rc.conf")
    # enable ezjail
    run("echo ezjail_enable='YES' >> /etc/rc.conf")
    # create admin user
    if "sudo" not in pkg_info:
        puts("Installing sudo")
        run("pkg_add -r sudo")
    if "no such user" in user_info:
        puts("Creating admin user %s" % admin)
        run("pw useradd -n %(admin)s -u 1001 -m -d /home/%(admin)s -G wheel" % dict(admin=admin))
        ssh_config = path.join('/', 'usr', 'home', admin, '.ssh')
        run("mkdir -p %s" % ssh_config)
        run("chown -R %s %s" % (admin, ssh_config))
        remote_keyfile = path.join(ssh_config, 'authorized_keys')
        put(keyfile, remote_keyfile)
        run("echo '%wheel ALL=(ALL) NOPASSWD: ALL' >> /usr/local/etc/sudoers")
    else:
        puts("Not touching existing user %s" % admin)

    # disable root login
    puts("Setting up ssh login")
    run("grep -v PermitRootLogin /etc/ssh/sshd_config > /etc/ssh/sshd_config.tmp")
    run("echo 'PermitRootLogin no' >> /etc/ssh/sshd_config.tmp")
    run("mv /etc/ssh/sshd_config /etc/ssh/sshd_config.bak")
    run("mv /etc/ssh/sshd_config.tmp /etc/ssh/sshd_config")
    run("echo sshd_enable='YES' >> /etc/rc.conf")
    run("/etc/rc.d/sshd restart")
    puts("You now should be able to login with `ssh %s`" % primary_ip)


@task
def install(source='pkg_add', jailzfs=None, **kw):
    """ assuming bootstrap has been run, install ezjail and run ezjail-admin install.

    if `source` is 'pkg_add' it installs a binary package, if it's 'cvs' it install from current CVS:

    if `jailzfs` is set, assume using ZFS and set the jailzfs path in ezjails configuration.

    all **kw are passed to `ezjail-admin install`. i.e. to install with ports (`-p`):

    ezjail-remote install:p=True

    """
    # install ezjail
    pkg_info = run("pkg_info")
    if "ezjail" not in pkg_info:
        puts("Installing ezjail (this could take a while")
        if source == 'cvs':
            run("cvs -d :pserver:anoncvs@cvs.erdgeist.org:/home/cvsroot co ezjail")
            with cd("ezjail"):
                sudo("make install")
        else:
            sudo("pkg_add -r ezjail")
        sudo("cp /usr/local/etc/ezjail.conf.sample /usr/local/etc/ezjail.conf")
        if jailzfs:
            sudo("""echo 'ezjail_use_zfs="YES"' >> /usr/local/etc/ezjail.conf""")
            sudo("""echo 'ezjail_jailzfs="%s"' >> /usr/local/etc/ezjail.conf""" % jailzfs)

        # run ezjail's install command
        install_basejail = "%s install%s" % (EZJAIL_ADMIN, kwargs2commandline(kw,
            boolflags=['p', 'P', 'm', 'M', 's', 'S']))
        sudo(install_basejail)
        sudo("echo 'ezjail_enable=YES' >> /etc/rc.conf")


@task
def create(name,
    ip,
    admin=None,
    keyfile=None,
    flavour=None,
    ctype=None,
    **kw):

    """<name>,<ip>(,<admin>,<keyfile>,flavour)

    Create a jail instance with the given name and IP address.
    Configures ssh access for the given admin user and ssh key.

    admin: defaults to the current user
    keyfile: defaults to ~/.ssh/identity.pub
    flavour: defaults to 'basic' and refers to a LOCAL flavour, NOT any on the host
    ctype: defaults to None and refers to the `-c` flag, meaning, you can set it to `simple`, `bde`, `eli` or `zfs`.

    any additional keyword arguments are passed to the flavour
    """

    if admin is None:
        admin = env['local_user']

    if keyfile is None:
        keyfile = path.expanduser("~/.ssh/identity.pub")

    if not path.exists(keyfile):
        sys.exit("No such keyfile '%s'" % keyfile)

    print("name: %s, ip: %s, flavour: %s" % (name, ip, flavour))
    from ezjailremote.flavours import basic
    local_flavour_path = path.abspath(path.dirname(basic.__file__))

    with settings(show("output"), warn_only=True):
        tmp_flavour = 'basic-%s' % datetime.now().strftime('%Y%m%d%H%M%s')
        remote_flavour_path = path.join(EZJAIL_JAILDIR, 'flavours', tmp_flavour)
        sudo("mkdir -p %s" % remote_flavour_path)
        sudo("chown %s %s" % (env['user'], remote_flavour_path))
        put("%s/*" % local_flavour_path, remote_flavour_path)
        local_flavour_script = path.join(local_flavour_path, 'ezjail.flavour')
        upload_template(local_flavour_script,
            path.join(remote_flavour_path, 'ezjail.flavour'),
            context=locals(), backup=False)
        # create the jail using the uploaded flavour
        if ctype:
            ctype = ' -c %s' % ctype
        else:
            ctype = ''
        create_jail = sudo("%s create -f %s%s %s %s" % (EZJAIL_ADMIN, tmp_flavour, ctype, name, ip))
        if create_jail.succeeded:
            jail_path = path.join(EZJAIL_JAILDIR, name)
            # copy resolv.conf from host
            sudo("cp /etc/resolv.conf %s" % path.join(jail_path, 'etc', 'resolv.conf'))
            # copy the key file into flavour
            ssh_config = path.join(jail_path, 'home', admin, '.ssh')
            sudo("mkdir -p %s" % ssh_config)
            remote_keyfile = path.join(ssh_config, 'authorized_keys')
            sudo("chown -R %s %s" % (admin, ssh_config))
            put(keyfile, remote_keyfile)
            sudoers = path.join(jail_path, 'usr', 'local', 'etc', 'sudoers')
            sudo("chown 0 %s" % sudoers)
            sudo("chmod 0440 %s" % sudoers)
            # start up the jail:
            sudo("%s start %s" % (EZJAIL_RC, name))
            # perform any additional setup the flavour may provide
            if flavour is not None:
                jexec(ip, apply_flavour, flavour, **kw)
        sudo("rm -rf %s" % remote_flavour_path)


@task
def apply_flavour(flavour, *args, **kwargs):
    flavour_module = get_flavour(flavour)
    if hasattr(flavour_module, 'setup'):
        flavour_module.setup(*args, **kwargs)


@task
def show_info():
    with settings(show("output"), warn_only=True):
        run("hostname")
        # run("ifconfig")


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


@task(default=True, aliases=['archive', 'config', 'console', 'delete', 'list', 'restore', 'update', 'start', 'stop'])
def usage(*xargs, **kw):
    """(passed directly to ezjail-admin)"""
    command = env.get('command')
    if command == 'usage':
        command = '--help'
    args_string = ''
    for item in kw.items():
        args_string += '%s %s ' % item
    with show('output'):
        sudo("%s %s %s %s" % (EZJAIL_ADMIN, command, args_string, ' '.join(xargs)))


@task
def jls():
    with show('output'):
        run("jls")
