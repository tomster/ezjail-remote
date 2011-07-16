import doctest
import unittest2

optionflags = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

def test_suite():
    suite = unittest2.TestSuite()
    suite.addTest(doctest.DocFileSuite('test_commandline.txt', optionflags=optionflags))
    return suite
