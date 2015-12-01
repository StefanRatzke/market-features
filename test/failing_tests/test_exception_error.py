import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePluginException(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        raise Exception("failing in loading test class")

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_next_one(self):
        """this test will not run due to setUpclass error"""
        self.another_error_should_cause_error()
        assert_equals(1, 1)
