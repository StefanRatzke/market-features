import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePluginNext(unittest2.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_next_one(self):
        '''another test module with some test, this is the first test'''
        assert_equals(1, 1)

    def test_next_two(self):
        '''another test module with some test, this is the seconde test'''
        assert_equals(1, 1)

    def test_next_three(self):
        '''another test module with some test, this is the third test, simulation failing test'''
        assert_equals(1, 1)
