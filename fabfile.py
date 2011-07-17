import sys
from os import path
from datetime import datetime

from fabric.api import run, sudo, put, env, settings
from fabric.state import output

EZJAIL_JAILDIR = '/usr/jails'
EZJAIL_RC = '/usr/local/etc/rc.d/ezjail.sh'

env['shell'] = '/bin/sh -c'
output['running'] = False


def jls():
    run('jls')

def create(name, 
    ip,
    admin=None,
    keyfile=None, 
    flavour=u'basic'):

    if admin is None:
        admin = env['local_user']
    
    print("name: %s, ip: %s, flavour: %s" % (name, ip, flavour))
    local_flavour_path = path.abspath(path.join('flavours', flavour))
    if not path.exists(local_flavour_path):
        sys.exit("No such flavour '%s'" % local_flavour_path)

    with settings(warn_only=True):

        tmp_flavour = '%s-%s' % (flavour, datetime.now().strftime('%Y%m%d%H%M%s'))
        remote_flavour_path = path.join(EZJAIL_JAILDIR, 'flavours', tmp_flavour)
        sudo("mkdir %s" % remote_flavour_path)
        sudo("chown %s %s" % (env['user'], remote_flavour_path))
        put("%s/*" % local_flavour_path, remote_flavour_path)
        # create on-the-fly flavour:
        # create the jail with the flavour
        
        create_jail = sudo("ezjail-admin create -f %s %s %s" % (tmp_flavour, name, ip))
        if create_jail.succeeded:
            sudo("%s start %s" % (EZJAIL_RC, name))
            #  * create the user
            #  * copy the key file into flavour
            #  * copy resolv.conf from host
            # start it up
        sudo("rm -rf %s" % remote_flavour_path)
