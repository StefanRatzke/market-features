from unittest import skip

import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestSkippy(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @skip('not yet implemented - testing skip')
    def test_next_one(self):
        assert_equals(1, 1)

    @skip('not yet implemented 2')
    def test_next_two(self):
        assert_equals(1, 1)
