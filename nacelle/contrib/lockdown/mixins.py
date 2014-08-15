"""Simple handler mixin to enforce HTTP basic auth
"""
# marty mcfly imports
from __future__ import absolute_import

# third-party imports
import webapp2

# local imports
from .utils import check_auth


class LockedDownMixin(object):
    """Simple mixin that enforces HTTP basic auth for a request handler
    """

    lockdown_username = None
    lockdown_password = None

    def dispatch(self):

        if not check_auth(self.request, self.lockdown_username, self.lockdown_password):
            m = 'Could not verify your access level for that URL. ' \
                'You have to login with proper credentials'
            resp = webapp2.Response(m)
            resp.set_status(401)
            resp.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'
            return resp
        super(LockedDownMixin, self).dispatch()
