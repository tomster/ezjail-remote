from fabric.api import run

def setup(name, ip, admin, keyfile, **kw):
    """ This method is called immediately after starting up the jail.
    Any additional keyword arguments passed to the create command from the command
    line are available here in kw
    """

