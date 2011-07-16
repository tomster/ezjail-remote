import sys
import StringIO


class StdOut(StringIO.StringIO):
    """ A StringIO based stdout replacement that optionally mirrors all
        output to stdout in addition to capturing it.
    """

    def __init__(self, stdout):
        self.__stdout = stdout
        StringIO.StringIO.__init__(self)

    def write(self, s):
        # uncomment the following for debugging tests!
        # self.__stdout.write(s)
        StringIO.StringIO.write(self, s)


class CommandLayer(object):

    """ this layer silences all stdout output during testruns, to avoid noise
    when running tests that invoke commands."""

    def testSetUp(self):
        self.out = StdOut(sys.stdout)
        self.err = StdOut(sys.stdout)
        sys.stdout = self.out
        sys.stderr = self.err
    testSetUp = classmethod(testSetUp)

    def testTearDown(self):
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    testTearDown = classmethod(testTearDown)

