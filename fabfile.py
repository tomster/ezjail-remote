from fabric.api import run

def jls():
    run('/usr/sbin/jls', shell=False)
