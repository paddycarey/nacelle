"""
Custom dispatcher for nacelle that implements lockdown support
"""
# marty mcfly imports
from __future__ import absolute_import

# stdlib imports
import re

# third-party imports
import webapp2
from nacelle.conf import settings
from nacelle.core.dispatcher import nacelle_dispatcher

# local imports
from .utils import check_auth


def compile_url_exceptions(url_exceptions):
    return [re.compile(p) for p in url_exceptions]

_default_url_exceptions = compile_url_exceptions(settings.LOCKDOWN_URL_EXCEPTIONS)


def lockdown_dispatcher(router, request, response):
    """Override dispatch to provide lockdown support
    """

    username = settings.LOCKDOWN_USERNAME
    password = settings.LOCKDOWN_PASSWORD

    # Don't lock down if the URL matches an exception pattern.
    unlocked_url = False
    for pattern in _default_url_exceptions:
        if pattern.search(request.path):
            unlocked_url = True
            break

    if not unlocked_url and not check_auth(request, username, password):
        msg = 'Could not verify your access level for that URL. ' \
            'You have to login with proper credentials'
        resp = webapp2.Response(msg)
        resp.set_status(401)
        resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
        return resp

    # Dispatch the request using nacelle's regular dispatcher.
    return nacelle_dispatcher(router, request, response)
