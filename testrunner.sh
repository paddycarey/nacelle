#!/bin/bash
set -e

coverage run --source="nacelle" --omit="google_appengine/*,nacelle/vendor/*" nacelle/test/runner.py
coverage report -m
