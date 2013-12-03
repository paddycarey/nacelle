"""
Test nacelle's authentication decorators
"""
# stdlib imports
import os

# third-party imports
import webapp2

# local imports
from nacelle.conf import settings
from nacelle.core.decorators import login_admin
from nacelle.core.decorators import login_cron
from nacelle.core.decorators import login_task
from nacelle.test.testcases import NacelleTestCase


# convenience fucntions to make logging a user in or out easier

def setCurrentUser(email, user_id, is_admin=False):
    """Convenience function to mock a logged in user
    """
    os.environ['USER_EMAIL'] = email or ''
    os.environ['USER_ID'] = user_id or ''
    os.environ['USER_IS_ADMIN'] = '1' if is_admin else '0'

def logoutCurrentUser():
    """Set currently mocked login to None
    """
    setCurrentUser(None, None)


# test fixtures: we need to set up a local wsgi app so we can test the login
# decorators against real handlers

@login_admin
def t_admin(request):
    """Test fixture to allow testing of @login_admin decorator
    """
    return webapp2.Response('success')


@login_cron
def t_cron(request):
    """Test fixture to allow testing of @login_cron decorator
    """
    return webapp2.Response('success')


@login_task
def t_task(request):
    """Test fixture to allow testing of @login_task decorator
    """
    return webapp2.Response('success')


# Define our WSGI app so GAE can run it
routes = [('/t_admin', t_admin), ('/t_cron', t_cron), ('/t_task', t_task)]
wsgi = webapp2.WSGIApplication(routes, debug=True, config={
    'webapp2_extras.sessions': {'secret_key': 'xxxxxxxxxxxxxxxxxxxxxx'}
})

# attach dispatcher and error_handler to the WSGI app
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
wsgi.router.set_dispatcher(dispatcher)


class LoginCronDecoratorTests(NacelleTestCase):

    def test_cron_decorator_unauthed_user(self):
        """Test that an unauthed user cannot access a protected cron URL
        """
        response = wsgi.get_response('/t_cron')
        self.assertEqual(401, response.status_int)

    def test_cron_decorator_authed_admin(self):
        """Test that an authed user (with admin rights) can access a protected cron URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=True)
        response = wsgi.get_response('/t_cron')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)
        logoutCurrentUser()

    def test_cron_decorator_authed_user(self):
        """Test that an authed user (without admin rights) cannot access a protected cron URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=False)
        response = wsgi.get_response('/t_cron')
        self.assertEqual(401, response.status_int)
        logoutCurrentUser()

    def test_cron_decorator_cronjob(self):
        """Test that a cronjob request can access a protected cron URL
        """
        response = wsgi.get_response('/t_cron', headers=[('X-Appengine-Cron', 'true')])
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class LoginTaskDecoratorTests(NacelleTestCase):

    def test_task_decorator_unauthed_user(self):
        """Test that an unauthed user cannot access a protected task URL
        """
        response = wsgi.get_response('/t_task')
        self.assertEqual(401, response.status_int)

    def test_task_decorator_authed_admin(self):
        """Test that an authed user (with admin rights) can access a protected task URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=True)
        response = wsgi.get_response('/t_task')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)
        logoutCurrentUser()

    def test_task_decorator_authed_user(self):
        """Test that an authed user (without admin rights) cannot access a protected task URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=False)
        response = wsgi.get_response('/t_task')
        self.assertEqual(401, response.status_int)
        logoutCurrentUser()

    def test_task_decorator_cronjob(self):
        """Test that a taskqueue request can access a protected task URL
        """
        response = wsgi.get_response('/t_task', headers=[('X-AppEngine-TaskName', 'true')])
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)


class LoginAdminDecoratorTests(NacelleTestCase):

    def test_admin_decorator_unauthed_user(self):
        """Test that an unauthed user gets redirected when attempting to access a protected URL
        """
        response = wsgi.get_response('/t_admin')
        self.assertEqual(302, response.status_int)
        self.assertTrue(response.headers['Location'].startswith('https://www.google.com/accounts/Login'))

    def test_admin_decorator_authed_admin(self):
        """Test that an authed user (with admin rights) can access a protected URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=True)
        response = wsgi.get_response('/t_admin')
        self.assertEqual(200, response.status_int)
        self.assertEqual('success', response.body)
        logoutCurrentUser()

    def test_admin_decorator_authed_user(self):
        """Test that an authed user (without admin rights) cannot access a protected URL
        """
        setCurrentUser('test@test.com', '1234567890', is_admin=False)
        response = wsgi.get_response('/t_admin')
        self.assertEqual(401, response.status_int)
        logoutCurrentUser()
