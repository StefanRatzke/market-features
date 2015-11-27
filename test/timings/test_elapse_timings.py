import time

import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class ElapseTimes(unittest2.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_wait_for_1_sec(self):
        time.sleep(1)
        assert_equals(1, 1)

    def test_wait_for_2_sec(self):
        time.sleep(2)
        assert_equals(1, 1)
