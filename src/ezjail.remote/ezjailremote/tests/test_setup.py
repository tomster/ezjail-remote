import unittest2

class BasicSetupTests(unittest2.TestCase):

    def test_main_command(self):
        from ezjailremote.command import main
        main()
