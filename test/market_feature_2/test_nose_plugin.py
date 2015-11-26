import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePlugin(unittest2.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_one(self):
        assert_equals(1, 1)

    def test_two(self):
        assert_equals(1, 2)
