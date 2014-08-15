"""Simple handler decorator to enforce HTTP basic auth
"""
# marty mcfly imports
from __future__ import absolute_import

# third-party imports
import webapp2

# local imports
from .utils import check_auth


def locked_down(username, password):
    """
    Decorator that locks down the wrapped view
    """
    def real_decorator(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if not check_auth(request, username, password):
                m = 'Could not verify your access level for that URL. ' \
                    'You have to login with proper credentials'
                resp = webapp2.Response(m)
                resp.set_status(401)
                resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
                return resp
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return real_decorator
