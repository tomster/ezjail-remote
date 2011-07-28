from os import path
from fabric import main

here = path.abspath(path.dirname(__file__))

def this_fabfile():
    return path.join(here, 'fabfile.py')

def commandline():
    main.find_fabfile = this_fabfile
    main.main()
