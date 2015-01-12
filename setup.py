from setuptools import setup

setup(
    name='market-features',
    version='0.1',
    author='Stefan Ratzke',
    author_email = 'stefan-ratzke@t-online.de',
    url = 'https://github.com/StefanRatzke/market-features',
    download_url = 'https://github.com/StefanRatzke/market-features/tarball/0.1',
    packages=['market_features'],
    description = 'Create HTML Test Results Report',
    license = '',
    entry_points = '''
        [nose.plugins.0.10]
        market_features = market_features:MarketFeatures
        ''',
    package_data={'market_features' : ['market_features.html.jinja']},
    install_requires = ['Jinja2 >=2.6, < 3.0'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
	'Environment :: Console',
	'Intended Audience :: Developers',
	'Natural Language :: English',
	'License :: OSI Approved :: Apache Software License',
	'Operating System :: OS Independent',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.7',
	'Topic :: Software Development :: Testing'
    ],
)
