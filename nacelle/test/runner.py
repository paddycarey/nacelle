#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test runner for nacelle
"""
# stdlib imports
import os
import sys

# third-party imports
import nose


# Fix the path
base_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    os.pardir, os.pardir))

sys.path.insert(0, base_dir)


# setup our appengine environment so we can import the libs we need for our tests,
# we need to do this first so we can import the stubs from testbed
from nacelle.test.environ import setup_environ
setup_environ()


if __name__ == '__main__':

    res = nose.run(argv=[
        'testrunner.py',
        '-v',
        '--with-yanc',
        '--logging-level=INFO'
    ])
    sys.exit(int(not res))
