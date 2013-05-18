"""
Base handlers
"""
# stdlib imports
import json
import logging
import sys
import urllib

# third-party imports
import webapp2
from google.appengine.api import taskqueue
from google.appengine.api import users
from httplib import HTTPException
from raven import Client
from webapp2_extras import jinja2
from webapp2_extras import sessions

# local imports
import settings
from nacelle.utils.encoder import ModelEncoder
from nacelle.utils.request import modify_query_string
from nacelle.utils.request import nav_match
from nacelle.utils.stringutils import prettify_string

# check if sentry enabled
if settings.SENTRY_DSN:
    client = Client(settings.SENTRY_DSN)
else:
    client = None


class BaseHandler(webapp2.RequestHandler):

    """
    Simple webapp2 base handler that reports exceptions
    to a sentry server if configured and provides session support
    """

    def dispatch(self):

        """
        Override dispatch() to provide session support
        """

        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def handle_exception(self, exception, debug):

        # build our error report
        error_report = {
            'method': self.request.method,
            'url': self.request.path_url,
            'query_string': self.request.query_string,
            # 'data': environ.get('wsgi.input'),
            'headers': dict(self.request.headers),
            'env': dict((
                ('REMOTE_ADDR', self.request.environ['REMOTE_ADDR']),
                ('SERVER_NAME', self.request.environ['SERVER_NAME']),
                ('SERVER_PORT', self.request.environ['SERVER_PORT']),
            )),
        }
        interface = 'sentry.interfaces.Http'

        if client is not None:
            try:
                exc_id = client.get_ident(client.captureException(data={interface: error_report}))
                logging.error('Error reported to sentry: %s' % str(exc_id))
            except HTTPException:
                logging.warning('Unable to contact sentry server')


class JsonHandler(BaseHandler):

    """
    Simple webapp2 base handler to return JSON data from API endpoints
    """

    def render_response(self, context):

        """
        Accepts a JSON encoded string or object which can be serialised to
        JSON and outputs it to the response as a JSON encoded string.
        """

        # if object is a string just return as is
        if isinstance(context, basestring):
            self.response.write(context)
        # else attempt to serialise and return
        else:
            context = json.dumps(context, cls=ModelEncoder)
            self.response.write(context)
        # set the right content-type header
        self.response.headers['Content-Type'] = 'application/json'
        # CORS Headers, 'cos that's how we roll
        self.response.headers['Access-Control-Allow-Origin'] = '*'

    def handle_exception(self, exception, debug):

        # collect our error data
        exc_info = sys.exc_info()

        # If the exception is a HTTPException, use its error code.
        # Otherwise use a generic 500 error code.
        if isinstance(exception, webapp2.HTTPException):
            self.response.set_status(exception.code)
            return self.render_response({'status': exception.code, 'content': str(exc_info[1])})

        # set status to 500 and set error response
        self.response.set_status(500)
        self.render_response({'status': 500, 'content': 'A server error has occurred'})
        # send error to sentry server and log it
        super(JsonHandler, self).handle_exception(exception, debug)
        logging.exception(exception)
        del exc_info


class TemplateHandler(BaseHandler):

    """
    Base handler for all handlers that require templating support
    """

    def default_context(self):

        """
        Returns a dictionary containing default
        context for all render calls
        """

        context = {
            # add request and session objects to default context
            'request': self.request,
            'session': self.session,
            # a couple of utility functions to help with logic in templates
            'getattr': getattr,
            'hasattr': hasattr,
            'isinstance': isinstance,
            'json': json,
            'quote': urllib.quote_plus,
            # user details (if logged in)
            'user': users.get_current_user(),
            'logout_url': users.create_logout_url(self.request.path_qs),
            'uri_for': webapp2.uri_for,
            'modify_query_string': modify_query_string,
            'nav_match': nav_match,
            'prettify_string': prettify_string,
            'str': str,
            'unicode': unicode,
        }

        # return default context
        return context

    @webapp2.cached_property
    def jinja2(self):
        # Returns a Jinja2 renderer cached in the app registry.
        return jinja2.get_jinja2(app=self.app)

    def render_response(self, _template, context):

        """
        Renders a template and writes the result to the response.
        """

        # update context with default context
        context.update(self.default_context())
        # render template
        rv = self.jinja2.render_template(_template, **context)
        # write rendered template to response
        return self.response.write(rv)

    def handle_exception(self, exception, debug):

        super(TemplateHandler, self).handle_exception(exception, debug)
        webapp2.RequestHandler.handle_exception(self, exception, debug)


class CronHandler(BaseHandler):

    """
    This handler reprocess all tags on videos each time it is called by cron, updating
    each tag in the datastore with its current weight and label
    """

    def get(self, *args, **kwargs):

        if not users.is_current_user_admin() and not 'X-AppEngine-TaskName' in self.request.headers:
            message = "Only admin users or cronjobs can access this URL"
            return self.abort(403, detail=message)

        if 'defer' in self.request.GET:
            return self.defer()

        return self.handle(*args, **kwargs)

    def post(self, *args, **kwargs):

        if not 'X-AppEngine-TaskName' in self.request.headers:
            return self.abort(401, detail="Only taskqueues can POST to this URL")

        return self.get(*args, **kwargs)

    def handle(self, *args, **kwargs):
        raise NotImplementedError('CronHandler instances require a handle() method')

    def defer(self):

        """
        Simple method that runs this task on the feedfetcher backend asynchronously
        which helps us avoid silly appengine limitations like 30sec per request
        """

        taskqueue.add(url=self.request.path)
        return self.response.write("Task queued: %s" % self.request.path_url)

    def handle_exception(self, exception, debug):

        if not isinstance(exception, webapp2.HTTPException):
            # send error to sentry server
            super(CronHandler, self).handle_exception(exception, debug)

        return webapp2.RequestHandler.handle_exception(self, exception, debug)
