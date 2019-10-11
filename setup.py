#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='psaudit',
    version='0.1.1',
    description='Process auditor for macOS',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Andrew Naoum',
    author_email='andy.naoum@gmail.com',
    url='https://github.com/anaoum/psaudit',
    scripts=['psaudit'],
    install_requires=['psutil>=5.6.3'],
    license='MIT',
    download_url='https://github.com/anaoum/psaudit/archive/0.1.1.tar.gz',
    classifiers=[
        'Operating System :: MacOS :: MacOS X',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
