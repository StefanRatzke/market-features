from unittest import skip

import unittest2
from nose.plugins.attrib import attr
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePlugin(unittest2.TestCase):

    @skip('skip one and error one')
    def test_one6(self):
        """first test, simulation passing test"""
        assert_equals(1, 1)
