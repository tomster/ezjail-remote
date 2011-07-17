from fabric.api import run

def jls():
    run('/usr/sbin/jls', shell=False)

def create(name, ip, admin=u'root', keyfile=None, flavour=None):
    print("name: %s, ip: %s, flavour: %s" % (name, ip, flavour))
    
    # create on-the-fly flavour:
    #  * create the user
    #  * copy the key file into flavour
    #  * copy resolv.conf from host
    # create the jail with the flavour
    # start it up
