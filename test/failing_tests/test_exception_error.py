import unittest2
import nose
from nose.plugins.attrib import attr
import os, os.path
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePluginException(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        pass
        # raise Exception("failing in loading test class")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_next_one(self):
        self.another_error()
        assert_equals(1, 1)
