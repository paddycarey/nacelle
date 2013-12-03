"""
Test nacelle's authentication decorators
"""
# stdlib imports
import json

# third-party imports
import webapp2

# local imports
from nacelle.conf import settings
from nacelle.core.decorators import render_handlebars
from nacelle.core.decorators import render_jinja2
from nacelle.core.decorators import render_json
from nacelle.test.testcases import NacelleTestCase


# test fixtures: we need to set up a local wsgi app so we can test the login
# decorators against real handlers

@render_jinja2('index.html')
def r_jinja2(request):
    """Test fixture to allow testing of @render_jinja2 decorator
    """
    return {'rendered_with': 'Jinja2'}


@render_jinja2('index.html')
def r_jinja2_r(request):
    """Test fixture to allow testing of @render_jinja2 decorator
    """
    return webapp2.Response('success')


@render_json
def r_json(request):
    """Test fixture to allow testing of @render_json decorator
    """
    return {'rendered_as': 'json'}


@render_json
def r_json_r(request):
    """Test fixture to allow testing of @render_json decorator
    """
    return webapp2.Response('success')


@render_json
def r_json_err(request):
    """Test fixture to allow testing of @render_json decorator
    """
    return webapp2.abort(405)


@render_handlebars('index.html')
def r_handlebars(request):
    """Test fixture to allow testing of @render_handlebars decorator
    """
    return {'rendered_with': 'Handlebars'}


@render_handlebars('index.html')
def r_handlebars_r(request):
    """Test fixture to allow testing of @render_handlebars decorator
    """
    return webapp2.Response('success')


# Define our WSGI app so GAE can run it
routes = [('/r_jinja2', r_jinja2), ('/r_json', r_json), ('/r_handlebars', r_handlebars), ('/r_jinja2_r', r_jinja2_r), ('/r_json_err', r_json_err), ('/r_json_r', r_json_r), ('/r_handlebars_r', r_handlebars_r)]
wsgi = webapp2.WSGIApplication(routes, debug=True, config={
    'webapp2_extras.sessions': {'secret_key': 'xxxxxxxxxxxxxxxxxxxxxx'}
})

# attach dispatcher and error_handler to the WSGI app
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
wsgi.router.set_dispatcher(dispatcher)


class RenderHandlebarsDecoratorTests(NacelleTestCase):

    def test_render_handlebars_existing_template(self):
        """Test rendering a template with Handlebars (pybars)
        """
        response = wsgi.get_response('/r_handlebars')
        self.assertEqual(200, response.status_int)
        self.assertIn('This template was rendered with Handlebars.', response.body)

    def test_render_handlebars_override_response(self):
        """Test that a webapp2.Response is rendered when explicitly returned from a handlebars handler
        """
        response = wsgi.get_response('/r_handlebars_r')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class RenderJinja2DecoratorTests(NacelleTestCase):

    def test_render_jinja2_existing_template(self):
        """Test rendering a template with Jinja2
        """
        response = wsgi.get_response('/r_jinja2')
        self.assertEqual(200, response.status_int)
        self.assertIn('This template was rendered with Jinja2.', response.body)

    def test_render_jinja2_override_response(self):
        """Test that a webapp2.Response is rendered when explicitly returned from a jinja2 handler
        """
        response = wsgi.get_response('/r_jinja2_r')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class RenderJsonDecoratorTests(NacelleTestCase):

    def test_render_json(self):
        """Test rendering a JSON response
        """
        response = wsgi.get_response('/r_json')
        self.assertEqual(200, response.status_int)
        self.assertDictEqual({'rendered_as': 'json'}, json.loads(response.body))

    def test_render_json_error(self):
        """Test that an error response is correctly rendered whena  JSON handler is aborted
        """
        response = wsgi.get_response('/r_json_err')
        self.assertEqual(405, response.status_int)
        self.assertDictEqual({u'error': u'405 Method Not Allowed'}, json.loads(response.body))

    def test_render_json_override_response(self):
        """Test that a webapp2.Response is rendered when explicitly returned from a json handler
        """
        response = wsgi.get_response('/r_json_r')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)
