"""
Main WSGI entry point to Nacelle
"""
# marty mc fly imports
from __future__ import absolute_import

# stdlib imports
import sys

# third-party imports
import webapp2

# local imports
from nacelle.conf import settings

# add vendor folder to the path so that we can load the modules it contains
sys.path.insert(0, settings.VENDOR_PATH)
for add_path in settings.ADDITIONAL_VENDOR_PATHS:
    sys.path.insert(0, add_path)

# use webapp2's import_string function to lazily import required modules for
# WSGI config
routes = webapp2.import_string(settings.ROUTES_MODULE)
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
error_handler = webapp2.import_string(settings.ERROR_HANDLER_MODULE)
secret_key_store = webapp2.import_string('nacelle.core.sessions.models.SecretKey')

# Define our WSGI app so GAE can run it
wsgi = webapp2.WSGIApplication(routes, debug=True, config={
    'webapp2_extras.sessions': {
        'secret_key': secret_key_store.get_key(),
    },
    'webapp2_extras.jinja2': {
        'globals': settings.JINJA_GLOBALS,
    }
})

# attach dispatcher and error_handler to the WSGI app
wsgi.router.set_dispatcher(dispatcher)
wsgi.error_handlers[500] = error_handler
