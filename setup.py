#!/usr/bin/env python3

from distutils.core import setup

setup(
    name='psaudit',
    version='0.1.0',
    description='Process auditor for macOS',
    author='Andrew Naoum',
    author_email='andy.naoum@gmail.com',
    url='https://github.com/anaoum/psaudit',
    scripts=['psaudit'],
    install_requires=['psutil>=5.6.3'],
)
