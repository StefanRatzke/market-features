import os
import unittest2
import nose
from nose.tools import *
from market_features import MarketFeatures
from nose.plugins.base import Plugin
support = os.path.join(os.path.dirname(__file__), 'support')
argv = [__file__, '-v']
if __name__ == "__main__":
    nose.main(argv=argv+['--with-market-features'],addplugins=[MarketFeatures()])
