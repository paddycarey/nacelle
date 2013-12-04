#!/bin/bash
#
# Simple testrunner for nacelle using nose
# Produces coverage report that can be pushed to services like coveralls.io
#
set -e

coverage run --source="nacelle" --omit="google_appengine/*,nacelle/vendor/*" nacelle/test/runner.py
coverage report -m
