"""
Default settings for nacelle
"""
# stdlib imports
import os

# third-party imports
import webapp2
from google.appengine.api import users


# Convenience property to allow modules to quickly
# reference the project's root directory from anywhere
ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
ROOT_DIR = os.path.abspath(ROOT_DIR)


# Set debug mode based on whether we're running locally or not
try:
    DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Development')
except KeyError:
    DEBUG = True


# Details of sentry server for logging exceptions (set to None to disable)
SENTRY_DSN = None

# Python dotted path to the routes for the app
ROUTES_MODULE = 'routes.ROUTES'

# Python dotted path to the default dispatcher for the app
DISPATCHER_MODULE = 'nacelle.core.dispatcher.nacelle_dispatcher'

# Python dotted path to the default dispatcher for the app
ERROR_HANDLER_MODULE = 'nacelle.core.exception_handlers.handle_500'

# path to which third-party libraries have been installed
VENDOR_PATH = os.path.join(ROOT_DIR, 'nacelle', 'vendor')
ADDITIONAL_VENDOR_PATHS = ()

# variables/functions to inject into any jinja template
JINJA_GLOBALS = {'uri_for': webapp2.uri_for, 'logout_url': users.create_logout_url}

# i18n related settings
TRANSLATIONS_PATH = os.path.join(ROOT_DIR, 'translations')
TRANSLATIONS_SELECTOR = 'nacelle.core.utils.i18n.get_locale'

# This setting exists purely for testing purposes
TEST_SETTING = '12345'
