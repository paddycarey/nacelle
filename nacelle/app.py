"""
Main WSGI entry point to Nacelle
"""
# marty mc fly imports
from __future__ import absolute_import

# stdlib imports
import itertools

# third-party imports
import webapp2

# local imports
from nacelle.conf import settings

# use webapp2's import_string function to lazily import required modules for
# WSGI config
try:
    routes = webapp2.import_string(settings.ROUTES_MODULE)
except webapp2.ImportStringError:
    routes = []
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
error_handler_404 = webapp2.import_string(settings.ERROR_HANDLER_MODULE_404)
error_handler_500 = webapp2.import_string(settings.ERROR_HANDLER_MODULE_500)
secret_key_store = webapp2.import_string('nacelle.core.sessions.models.SecretKey')

# some of nacelle's contrib apps have routes, so we need to make sure and
# append those to our routes list before passing it into the WSGI app
mail_routes = webapp2.import_string('nacelle.contrib.mail.routes.ROUTES')
routes = list(itertools.chain(routes, mail_routes))

# Define our WSGI app so GAE can run it
wsgi = webapp2.WSGIApplication(routes, debug=settings.DEBUG, config={
    'webapp2_extras.sessions': {
        'secret_key': secret_key_store.get_key(),
    },
    'webapp2_extras.jinja2': settings.JINJA_SETTINGS,
    'webapp2_extras.i18n': {
        'translations_path': settings.TRANSLATIONS_PATH,
        'locale_selector': settings.TRANSLATIONS_SELECTOR,
    },
})

# attach dispatcher and error_handler to the WSGI app
wsgi.router.set_dispatcher(dispatcher)
wsgi.error_handlers[404] = error_handler_404
wsgi.error_handlers[500] = error_handler_500
