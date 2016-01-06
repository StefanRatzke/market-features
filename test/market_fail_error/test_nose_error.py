import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePlugin(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        raise Exception("error")

    def test_one(self):
        """first test, simulation passing test"""
        assert_equals(1, 1)
