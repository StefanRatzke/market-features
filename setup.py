from setuptools import setup

setup(
    name='market-features',
    version='0.5.6',
    author='Stefan Ratzke, Caleb Carvalho, Ralf Thaenert',
    author_email='stefan-ratzke@t-online.de',
    url='https://github.com/StefanRatzke/market-features',
    download_url='https://github.com/StefanRatzke/market-features/tarball/0.5.2',
    maintainer='Stefan Ratzke, Caleb Carvalho, Ralf Thaenert',
    maintainer_email='caleb.carvalho@gmail.com',
    packages=['market_features'],
    description='nosetest plug in to Create IntelliJ Style HTML Test Results Report',
    license='',
    entry_points='''
        [nose.plugins.0.10]
        market_features = market_features:MarketFeatures
        ''',
    package_data={'market_features': ['market_features.html.jinja','style.css','jquery-3.3.1.min.js','treeview.js']},
    include_package_data=True,
    install_requires=['Jinja2 >=2.6, < 3.0'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Testing'
    ],
)
