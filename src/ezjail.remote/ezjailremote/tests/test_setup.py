import unittest2

from ezjailremote.command import ezjailremote
from ezjailremote.tests import CommandLayer

class BasicSetupTests(unittest2.TestCase):

    layer = CommandLayer

    def test_calling_main_command(self):
        ezjailremote()
