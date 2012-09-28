"""Usage:
    ezdeploy create [options] (TARGET TARGET)...
    ezdeploy configure  (TARGET TARGET)...
    ezdeploy update  (TARGET TARGET)...
    ezdeploy destroy JAIL

Deploy a jail host and/or jail(s).

Options:
    -b , --blueprints FILE     path to the blueprint python file [default: blueprints.py]
    -c, --config FILE          path to config file [default: jails.conf]
    -h, --help                 show this message

"""


from docopt import docopt


def commandline():
    arguments = docopt(__doc__)
    print arguments

if __name__ == '__main__':
    commandline()
