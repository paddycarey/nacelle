# stdlib imports
import logging
from httplib import HTTPException

# third-party imports
from raven import Client

# local imports
from nacelle.conf import settings

# check if sentry enabled
if settings.SENTRY_DSN:
    client = Client(settings.SENTRY_DSN)
else:
    client = None


def handle_500(request, response, exception):

    """
    Report any uncaught errors to sentry and let the user know something's gone
    wrong
    """

    # build our error report
    error_report = {
        'method': request.method,
        'url': request.path_url,
        'query_string': request.query_string,
        'data': dict(request.POST),
        'headers': dict(request.headers),
        'env': dict((
            ('REMOTE_ADDR', request.environ['REMOTE_ADDR']),
            ('SERVER_NAME', request.environ['SERVER_NAME']),
            ('SERVER_PORT', request.environ['SERVER_PORT']),
        )),
    }
    interface = 'sentry.interfaces.Http'

    response.write('A server error occurred: ')
    response.set_status(500)

    if client is not None:
        try:
            exc_id = client.get_ident(client.captureException(data={interface: error_report}))
            logging.error('Error reported to sentry: %s' % str(exc_id))
            response.write(str(exc_id))
        except HTTPException:
            logging.warning('Unable to contact sentry server')

    logging.exception(exception)
