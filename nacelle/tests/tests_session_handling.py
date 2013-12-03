"""
Test nacelle's session handling
"""
# third-party imports
import webapp2

# local imports
from nacelle.conf import settings
from nacelle.test.testcases import NacelleTestCase


# test fixtures: we need to set up a local wsgi app so we can test the login
# decorators against real handlers

def set_session_var(request):
    session = request.session()
    session['test'] = 'just testing'
    return webapp2.Response('success')


def get_session_var(request):
    session = request.session()
    return webapp2.Response(session.get('test', 'no sell :('))


# Define our WSGI app so GAE can run it
routes = [('/get_session_var', get_session_var), ('/set_session_var', set_session_var)]
wsgi = webapp2.WSGIApplication(routes, debug=True, config={
    'webapp2_extras.sessions': {'secret_key': 'xxxxxxxxxxxxxxxxxxxxxx'}
})

# attach dispatcher and error_handler to the WSGI app
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
wsgi.router.set_dispatcher(dispatcher)


class SessionHandlingTests(NacelleTestCase):

    def test_setting_session_var_and_retrieve_on_next_request(self):
        """Test persisting a session variable in a cookie
        """

        response = wsgi.get_response('/set_session_var')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

        # Can do the same for data, allowing you to store it as a map.
        headers = [('Cookie', response.headers['Set-Cookie'])]

        response = wsgi.get_response('/get_session_var', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('just testing', response.body)
