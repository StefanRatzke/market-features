import unittest2
import nose
from nose.plugins.attrib import attr
import os, os.path
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePluginNext(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def tearDown(self):
        pass

    def test_next_one(self):
        assert_equals(1, 1)
