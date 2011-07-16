import unittest2

from ezjailremote.tests import CommandLayer

class BasicSetupTests(unittest2.TestCase):

    layer = CommandLayer

    def test_main_command(self):
        from ezjailremote.command import ezjailremote as main
        main()
