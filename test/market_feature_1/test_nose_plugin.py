import time
import unittest2
import nose
from nose.plugins.attrib import attr
import os, os.path
from nose.tools import assert_equals


@attr('test_nose_plugin')
class TestNosePlugin(unittest2.TestCase):
    def setUp(self):    
        pass
        
    def tearDown(self):
        pass
    
    def test_one(self):
        '''first test, simulation passing test'''
        time.sleep(1)
        assert_equals(1,1)

    def test_two(self):
        assert_equals(1,1)
        
    def test_three(self):
        time.sleep(1)
        ''' third test, simulation failing test'''
        assert_equals(1,1)
        