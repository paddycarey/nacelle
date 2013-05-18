"""
Base utilities used throughout nacelle's API clients
"""
# marty mcfly imports
from __future__ import absolute_import

# stdlib imports
import logging

# third-party imports
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

# local imports
from nacelle.utils.exceptions import retry_on_exception


def make_authorized_request(url, credentials, retrying=False, auth_type=None, **urlfetch_params):

    """
    Authorize and execute a urlfetch.fetch request, using the given
    access token and params.
    """

    # Add required custom headers to the request
    if 'headers' in urlfetch_params:
        headers = urlfetch_params['headers']
        del urlfetch_params['headers']
    else:
        headers = {}
    if auth_type == 'authsub':
        headers['authorization'] = 'AuthSub token=' + credentials.access_token
    else:
        headers['authorization'] = 'OAuth ' + credentials.access_token

    # build and execute the request
    response = make_request(url, headers=headers, **urlfetch_params)
    if response.status_code == 403 and not retrying:
        credentials.refresh_auth()
        return make_authorized_request(url, credentials, retrying=True, headers=headers, **urlfetch_params)
    return response


@retry_on_exception((urlfetch_errors.DeadlineExceededError, urlfetch_errors.DownloadError), tries=6)
def make_request(url, **urlfetch_params):

    # build and execute the request
    response = urlfetch.fetch(url, **urlfetch_params)
    return response
