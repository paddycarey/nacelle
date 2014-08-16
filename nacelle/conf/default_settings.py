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
ROUTES_MODULE = 'app.ROUTES'

# Python dotted path to the default dispatcher for the app
DISPATCHER_MODULE = 'nacelle.core.dispatcher.nacelle_dispatcher'

# Python dotted path to the default dispatcher for the app
ERROR_HANDLER_MODULE_404 = 'nacelle.core.exception_handlers.handle_404'
ERROR_HANDLER_MODULE_500 = 'nacelle.core.exception_handlers.handle_500'

# default Jinja2 settings.
JINJA_SETTINGS = {
    'globals': {'uri_for': webapp2.uri_for, 'logout_url': users.create_logout_url},
}

# i18n related settings
TRANSLATIONS_PATH = os.path.join(ROOT_DIR, 'translations')
TRANSLATIONS_SELECTOR = 'nacelle.core.utils.i18n.get_locale'

# Taskqueue that should be used to send mail asynchronously
EMAIL_QUEUE = 'default'

# This setting exists purely for testing purposes
TEST_SETTING = '12345'
