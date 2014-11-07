from distutils.core import setup

setup(
    name='market-features',
    version='0.1',
    author='Stefan Ratzke',
    author_email = '',
    url = 'https://github.com/StefanRatzke/nose-market-features',
    packages=['market_features'],
    #package_dir={'market_features' : 'market_features'},
    description = 'Create HTML Test Results Report',
    license = '',
#    py_modules = ['market_features'],
    entry_points = {
        'nose.plugins.0.10': [
            'market_features = market_features:MarketFeatures'
            ]
        },
    package_data={'market_features' : ['market_features.html.jinja']},
    install_requires = ['Jinja2 >=2.6, < 3.0']
)
