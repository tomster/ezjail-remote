import sys
from os import path
from fabric import main

here = path.abspath(path.dirname(__file__))


def commandline():
    # default to our own fabfile
    if '-f' not in sys.argv:
        sys.argv.extend(['-f', path.join(here, 'fabfile.py')])
    main.main()
