from unittest import TestCase
import doctest


class DocTestCase(TestCase):

    def __new__(self, test):
        return getattr(self, test)()

    @classmethod
    def test_account(cls):
        return doctest.DocTestSuite("ezjailremote.utils")
