"""
Simple function decorators for common tasks (rendering templates/json, making requests deferrable, etc.)
"""
# third-party imports
import json
import logging
import webapp2
from google.appengine.api import taskqueue
from google.appengine.api import users

# local imports
from nacelle.core.exception_handlers import report_to_sentry
from nacelle.core.template.renderers import render_jinja2_template
from nacelle.core.utils.encoder import ModelEncoder


__all__ = ['render_jinja2', 'render_json']


def deferrable(queue_name):
    """
    Decorator that makes a request function deferrable by passing `?defer` in
    the url's query string. Decorated handlers will be restricted to logged-in
    admin users or taskqueues.
    """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            # check caller is authorised
            if not users.is_current_user_admin() and not 'X-AppEngine-TaskName' in request.headers:
                return webapp2.abort(401, detail="Only taskqueues or admin users can access URL")
            # check if the defer key was passed in the query string
            if 'defer' in request.GET:
                taskqueue.add(url=request.path)
                return webapp2.Response('Task queued: %s' % request.path)
            # call the view function
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


def render_jinja2(template_name):
    """
    Decorator that renders the decorated function with the given handlebars template.
    """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            # call the view function
            context = view_method(request, *args, **kwargs)
            # if the view has returned a HttpResponse or subclass then return that directly
            if issubclass(type(context), webapp2.Response):
                return context
            # add the current request to the context as it's useful when rendering
            context['request'] = request
            # load specified template and render it with the context
            output = render_jinja2_template(template_name, context)
            # return the rendered template wrapped in a webapp2 Response object
            return webapp2.Response(output)
        return _arguments_wrapper
    return _method_wrapper


def require_method(http_methods):
    """
    Decorator that enforces a HTTP method for the wrapped function
    """
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            if not request.method in http_methods:
                return webapp2.abort(405)
            # call the view function
            return view_method(request, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper


def render_json(view_method):
    """
    Decorator that renders the decorated function as JSON
    """
    def _arguments_wrapper(request, *args, **kwargs):
        try:
            context = view_method(request, *args, **kwargs)
            if isinstance(context, tuple):
                status = context[1]
                context = context[0]
            else:
                status = 200
        except webapp2.HTTPException as e:
            context = {'error': "%d %s" % (e.code, e.title), 'detail': e.detail}
            status = e.code
        except Exception as e:
            logging.exception(e)
            exc_id = report_to_sentry(request)
            context = {'error': "500 Server Error", 'detail': exc_id}
            status = 500
        if issubclass(type(context), webapp2.Response):
            return context
        response = webapp2.Response(json.dumps(context, cls=ModelEncoder))
        response.set_status(status)
        response.headers['Content-Type'] = 'application/json'
        return response
    return _arguments_wrapper


def login_admin(view_method):
    """
    Decorator that enforces admin login
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # check caller is authorised
        request.user = users.get_current_user()
        if not request.user:
            login_url = users.create_login_url(request.url)
            return webapp2.redirect(login_url)
        if not users.is_current_user_admin():
            return webapp2.abort(401, detail="Only admin users can access URL")
        # call the view function
        return view_method(request, *args, **kwargs)
    return _arguments_wrapper


def login_cron(view_method):
    """
    Decorator that ensures handler is only available to cronjobs
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # check caller is authorised
        if not users.is_current_user_admin() and not 'X-Appengine-Cron' in request.headers:
            return webapp2.abort(401, detail="Only cronjobs or admin users can access this URL")
        # call the view function
        return view_method(request, *args, **kwargs)
    return _arguments_wrapper


def login_task(view_method):
    """
    Decorator that ensures handler is only available to task queues
    """
    def _arguments_wrapper(request, *args, **kwargs):
        # check caller is authorised
        if not users.is_current_user_admin() and not 'X-AppEngine-TaskName' in request.headers:
            return webapp2.abort(401, detail="Only taskqueues or admin users can access this URL")
        # call the view function
        return view_method(request, *args, **kwargs)
    return _arguments_wrapper
