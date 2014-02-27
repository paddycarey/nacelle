"""
Test lockdown decorator
"""
# third-party imports
import webapp2

# local imports
from .utils import DecodeError
from .utils import decode
from .utils import encode
from .decorators import locked_down
from .mixins import LockedDownMixin
from nacelle.test.testcases import NacelleTestCase


# test fixtures: we need to set up a local wsgi app so we can test the
# decorator against real handlers

@locked_down('uname', 'pword')
def locked_handler(request):
    return webapp2.Response('success')


class LDTestHandler(LockedDownMixin, webapp2.RequestHandler):

    lockdown_username = 'uname'
    lockdown_password = 'pword'

    def get(self):
        self.response.write('success')


# Define our WSGI app so GAE can run it
routes = [('/', locked_handler), ('/ld', LDTestHandler)]

wsgi = webapp2.WSGIApplication(routes, debug=True, config={
    'webapp2_extras.sessions': {'secret_key': 'xxxxxxxxxxxxxxxxxxxxxx'}
})

# attach dispatcher and error_handler to the WSGI app
dispatcher = webapp2.import_string('nacelle.core.dispatcher.nacelle_dispatcher')
wsgi.router.set_dispatcher(dispatcher)


class LockdownDecoratorTests(NacelleTestCase):

    def test_properly_returns_401_when_no_headers(self):
        """@locked_down decorator returns a 401 when no auth headers present
        """
        response = wsgi.get_response('/')
        self.assertEqual(401, response.status_int)
        self.assertIn('WWW-Authenticate', response.headers)
        self.assertIn('Could not verify your access level for that URL. '
                      'You have to login with proper credentials', response.body)

    def test_properly_unlocks_when_valid_headers(self):
        """@locked_down allows access when auth headers are valid
        """
        headers = [('Authorization', encode('uname', 'pword'))]
        response = wsgi.get_response('/', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

    def test_properly_unlocks_when_valid_but_malformed_headers(self):
        """@locked_down allows access when auth headers are valid but missing BASIC prefix
        """
        auth_string = encode('uname', 'pword').replace('Basic ', '')
        headers = [('Authorization', auth_string)]
        response = wsgi.get_response('/', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class LockdownMixinTests(NacelleTestCase):

    def test_properly_returns_401_when_no_headers(self):
        """LockedDownMixin returns a 401 when no auth headers present
        """
        response = wsgi.get_response('/ld')
        self.assertEqual(401, response.status_int)
        self.assertIn('WWW-Authenticate', response.headers)
        self.assertIn('Could not verify your access level for that URL. '
                      'You have to login with proper credentials', response.body)

    def test_properly_unlocks_when_valid_headers(self):
        """LockedDownMixin allows access when auth headers are valid
        """
        headers = [('Authorization', encode('uname', 'pword'))]
        response = wsgi.get_response('/ld', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)

    def test_properly_unlocks_when_valid_but_malformed_headers(self):
        """LockedDownMixin allows access when auth headers are valid but missing BASIC prefix
        """
        auth_string = encode('uname', 'pword').replace('Basic ', '')
        headers = [('Authorization', auth_string)]
        response = wsgi.get_response('/ld', headers=headers)
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class Encode(NacelleTestCase):

    def test_prepends_basic_auth(self):
        self.assertTrue(encode('', '').lower().startswith('basic'))

    def test_adds_space_after_basic(self):
        self.assertTrue(encode('', '').lower().startswith('basic '))

    def test_encodes_short_username(self):
        self.assertTrue(encode('', 'password'))

    def test_encodes_short_password(self):
        self.assertTrue(encode('username', ''))

    def test_encodes_long_username(self):
        self.assertTrue(encode('username'*1000000, ''))

    def test_encodes_long_password(self):
        self.assertTrue(encode('', 'password'*1000000))


class Decode(NacelleTestCase):

    def test_decodes_empty_username(self):
        self.assertEqual('', decode(encode('', 'password'))[0])

    def test_decodes_empty_password(self):
        self.assertEqual('', decode(encode('username', ''))[1])

    def test_decodes_hashes_only(self):
        username, password = 'username', 'omgawesome!'
        encoded_str = encode(username, password)
        encoded_hash = encoded_str.split(' ')[1]
        self.assertEqual((username, password), decode(encoded_hash))

    def test_decodes_fully_encoded_strings(self):
        username, password = 'username', 'password'
        encoded_str = encode(username, password)
        self.assertEqual((username, password), decode(encoded_str))

    def test_doesnt_decode_invalid_auth_types(self):
        encoded_str = 'error woot'
        self.assertRaises(DecodeError, decode, encoded_str)

    def test_doesnt_decode_invalid_hashes(self):
        encoded_str = 'basic omg hacks what'
        self.assertRaises(DecodeError, decode, encoded_str)

        encoded_str = 'basic omg hacks'
        self.assertRaises(DecodeError, decode, encoded_str)

        encoded_str = 'basic omg'
        self.assertRaises(DecodeError, decode, encoded_str)

        encoded_str = 'basic'
        self.assertRaises(DecodeError, decode, encoded_str)

    def test_properly_escapes_colons(self):
        username, password = 'user:name:', 'pass:word:'
        encoded_str = encode(username, password)
        self.assertEqual((username, password), decode(encoded_str))
