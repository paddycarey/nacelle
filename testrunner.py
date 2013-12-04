#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test runner for nacelle
"""
# third-party imports
import nose

# setup our appengine environment so we can import the libs we need for our tests,
# we need to do this first so we can import the stubs from testbed
from nacelle.test.environ import setup_environ
setup_environ()


if __name__ == '__main__':

    nose.run(argv=[
        'testrunner.py',
        '-v',
        '--with-cover',
        '--cover-package=app,nacelle',
        '--cover-inclusive',
        '--cover-erase',
        '--with-yanc',
        '--logging-level=INFO'
    ])
