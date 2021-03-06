from setuptools import setup
import io
import os
import re
from ilabs.s3util import __version__, __description__, __url__, __author__, \
    __author_email__, __keywords__

NAME = 'ilabs.s3util'

setup(
    name=NAME,
    version=__version__,
    description=__description__,
    long_description='See ' + __url__,
    url=__url__,
    author=__author__,
    author_email=__author_email__,
    keywords=__keywords__,

    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=[NAME],
    install_requires=['boto3'],
    namespace_packages=['ilabs'],
    entry_points={
        'console_scripts': [
            's3pypi=ilabs.s3util.main_pypi:main',
            's3upload=ilabs.s3util.main_upload:main',
        ]
    }
)
