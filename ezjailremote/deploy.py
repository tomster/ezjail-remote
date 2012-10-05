"""Usage:
    ezjail-deploy [options] (bootstrap|install)
    ezjail-deploy [options] (init|prepare|configure|update|destroy) [JAIL]...

Deploy a jail host and/or jail(s).

Options:
    -b , --blueprints FILE   path to the blueprint python file [default: ./blueprints.py]
    -c, --config FILE        path to config file [default: ./jails.conf]
    -h, --help               show this message


Commands:
    boostrap: prepare a remote jail host via SSH.
    init: call the `create`, `prepare` and `update`` methods of all given jails.
        if no jail is specified, *all* jails are targetted.

    update: assumes that the jail's `create` and `prepare` methods have already run
        and executes their `update` method. if no jail is specified, *all* jails are
        targetted. it should be able to run a jail's `update` method more than once
        during the lifetime of a jail.
"""

import sys
from docopt import docopt
from fabric import api as fab
from os import path
import ConfigParser as ConfigParser_


class ConfigParser(ConfigParser_.SafeConfigParser):
    """ a ConfigParser that can provide its values as simple dictionary.
    taken from http://stackoverflow.com/questions/3220670
    """

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d


def commandline():
    # parse the command line arguments
    arguments = docopt(__doc__)

    # parse the configuration
    fs_config = arguments['--config']
    config = dict()
    if path.exists(fs_config):
        parser = ConfigParser(allow_no_value=True)
        parser.read(fs_config)
        parsed_dict = parser.as_dict()
        for key in parsed_dict.keys():
            if key in config:
                config[key].update(parsed_dict.get(key, dict()))
            else:
                config[key] = parsed_dict[key]

    # instantiate host and jails
    fs_dir, fs_blueprint = path.split(path.abspath(arguments['--blueprints']))
    sys.path.insert(0, fs_dir)
    blueprints = __import__(path.splitext(fs_blueprint)[0])
    # inject location of the config file so jails can resolve relative paths
    config['_fs_config'] = path.dirname(path.abspath(fs_config))
    jailhost = getattr(blueprints, config['host'].get('blueprint',
        'JailHost'))(blueprints, config)

    # 'point' fabric to the jail host
    fab.env['host_string'] = jailhost.ip_addr

    # execute the bootstrap and/or install command
    if arguments['bootstrap']:
        jailhost.bootstrap()
    if arguments['install'] or arguments['bootstrap']:
        jailhost.install()
        exit()

    # validate the jail name(s)
    jails = arguments['JAIL']
    config_jails = jailhost.jails.keys()
    alljails = set(config_jails).union(set(jailhost.available_blueprints))
    difference = set(jails).difference(alljails)
    if difference:
        print "invalid jail%s %s! (needs to be one of %s)" % \
            (len(difference) > 1 and 's' or '',
                ', '.join(list(difference)),
                ', '.join(list(alljails)))
        exit()

    # execute the jail command
    for jail_name in jails:
        jail = jailhost.jails[jail_name]
        if arguments['init']:
            jail.create()
            jail.prepare()
            jail.update()
        elif arguments['update']:
            jail.update()
        elif arguments['prepare']:
            jail.prepare()
        elif arguments['configure']:
            jail.configure()
        elif arguments['destroy']:
            jail.destroy()


if __name__ == '__main__':
    commandline()
