from setuptools import setup
from setuptools import find_packages

setup(
    name = 'stispixeldb',
    description = 'Create and Query STIS Pixel History Database',
    url = 'https://github.com/dougbrn/stis-ccd-pixeldb',
    author = 'Doug Branton, Colton Parker, Eddie Woods',
    author_email = 'dbranton@stsci.edu',
    classifiers = ['Programming Language :: Python',
                   'Intended Audience :: Science/Research',
                   'Topic :: Scientific/Engineering :: Astronomy',
                   'Topic :: Scientific/Engineering :: Physics',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
    package_dir={"": "stispixeldb"},
    packages=find_packages(where="stispixeldb"),
    install_requires = ['pandas', 'numpy', 'mysql-connector-python'],
    version = 0.0)