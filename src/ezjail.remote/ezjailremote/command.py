import optparse
import sys
import os

class Command(object):

    def __init__(self, ezjailremote):
        self.ezjailremote = ezjailremote


class CmdJls(Command):

    def __init__(self, ezjailremote, args=None):
        Command.__init__(self, ezjailremote)
        self.parser = optparse.OptionParser(
            usage = "%prog host jls",
            description = """
            """,
            add_help_option=False)
        self.parser.add_option("-v", "--verbose", dest="verbose",
            action="store_true", default=False,
            help="""Show remote output.""")

    def __call__(self):
        options, xargs = self.parser.parse_args(self.ezjailremote.args[2:])


class CmdHelp(Command):

    def __init__(self, ezjailremote):
        Command.__init__(self, ezjailremote)
        self.parser = optparse.OptionParser(
            usage="%prog help [<command>]",
            description="Show help on the given command or about the whole "
                "script if none given.",
            add_help_option=False)

    def __call__(self):
        ezjailremote = self.ezjailremote
        if len(ezjailremote.args) != 3 or ezjailremote.args[2] not in ezjailremote.commands:
            print("usage: %s <command> [options] [args]"
                % os.path.basename(ezjailremote.args[0]))
            print("\nType '%s help <command>' for help on a specific command."
                % os.path.basename(ezjailremote.args[0]))
            print("\nAvailable commands:")
            f_to_name = {}
            for name, f in ezjailremote.commands.iteritems():
                f_to_name.setdefault(f, []).append(name)
            for cmd in sorted(x for x in dir(ezjailremote) if x.startswith('cmd_')):
                name = cmd[4:]
                f = getattr(ezjailremote, cmd)
                aliases = [x for x in f_to_name[f] if x != name]
                if len(aliases): # pragma: no cover (until we actually have aliases)
                    print("    %s (%s)" % (name, ", ".join(aliases)))
                else:
                    print("    %s" % name)
        else:
            print ezjailremote.commands[ezjailremote.args[2]].parser.format_help()


class Remote(object):

    def __call__(self, **kwargs):

        self.cmd_jls = CmdJls(self)
        self.cmd_help = CmdHelp(self)

        self.commands = dict(
            jls=self.cmd_jls,
            help=self.cmd_help,
        )

        # allow sys.argv to be overridden (used for testing)
        if 'args' in kwargs:
            self.args = ['ezjailremote'] + kwargs['args']
        else:
            self.args = sys.argv

        # if no command was given, default to usage
        try:
            command = self.args[1]
        except IndexError:
            command = 'help'
        self.commands.get(command, self.unknown)()

    def unknown(self):
        print "Unknown command '%s'." % self.args[1]
        sys.exit(1)


ezjailremote = Remote()
