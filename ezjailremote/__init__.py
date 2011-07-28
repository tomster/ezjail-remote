from os import path
from fabric import main

def this_fabfile():
    return path.join(path.abspath(path.dirname(__file__)), 'fabfile.py')

def commandline():
    main.find_fabfile = this_fabfile
    main.main()
