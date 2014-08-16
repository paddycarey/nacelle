#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


setup(
    name='nacelle',
    version='0.4.1',
    description='A lightweight Python framework (built on top of webapp2) for use on Google Appengine',
    long_description=open('README.rst').read(),
    author='Patrick Carey',
    author_email='patrick@rehabstudio.com',
    url='https://github.com/nacelle/nacelle',
    packages=find_packages(),
    package_dir={'nacelle':
                 'nacelle'},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='nacelle',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
    ],
)
