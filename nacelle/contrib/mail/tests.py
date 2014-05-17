# -*- coding: utf-8 -*-
"""Tests for nacelle's mail functionality
"""
# marty mcfly imports
from __future__ import absolute_import

# stdlib imports
import base64

# third-party imports
import webapp2
from nacelle.conf import settings
from nacelle.test.testcases import NacelleTestCase

# local imports
from nacelle.contrib import mail
from nacelle.contrib.mail import routes


wsgi = webapp2.WSGIApplication(routes.ROUTES, debug=True, config={
    'webapp2_extras.sessions': {'secret_key': 'xxxxxxxxxxxxxxxxxxxxxx'},
})

# attach dispatcher and error_handler to the WSGI app
dispatcher = webapp2.import_string(settings.DISPATCHER_MODULE)
wsgi.router.set_dispatcher(dispatcher)


def _make_test_request(url, post_data=None, headers=None):
    """Make a test request against the app
    """
    request = webapp2.Request.blank(url, POST=post_data, headers=headers)
    return request.get_response(wsgi)


def _run_tasks(taskq_stub, q_name):
    """Since nose runs our tests single threaded, appengine can't run tests in
    the background, thus we need to run them manually at the appropriate point
    during our tests.
    """
    tasks = taskq_stub.GetTasks(q_name)
    taskq_stub.FlushQueue(q_name)
    while tasks:
        for task in tasks:
            params = base64.b64decode(task["body"])
            yield _make_test_request(task["url"], post_data=params, headers=[('X-AppEngine-TaskName', 'task1')])
        tasks = taskq_stub.GetTasks(q_name)
        taskq_stub.FlushQueue(q_name)


def _test_data(**overrides):
    """Returns a valid set of test data to use during API integration tests

    overrides allows the caller to replace one or more items in the returned
    dictionary without having to specify the entire thing every time.
    """
    test_data = {
        'sender': 'someemail@somedomain.com',
        'to': 'someotheremail@somedomain.com',
        'subject': 'Just a test email',
        'body': 'Just some test content'
    }
    for key, value in overrides.items():
        test_data[key] = value
    return test_data


class MailTests(NacelleTestCase):
    """Test nacelle's email functionality
    """

    def test_valid_email(self):
        """Test that sending a valid email succeeds
        """
        mail.send(**_test_data())

        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual('someotheremail@somedomain.com', messages[0].to)

    def test_valid_email_empty_body(self):
        """Test that sending a valid email (with an empty body) succeeds
        """
        mail.send(**_test_data(body=''))

        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual('someotheremail@somedomain.com', messages[0].to)

    def test_valid_email_no_body(self):
        """Test that sending a valid email (with no body) succeeds
        """
        _td = _test_data()
        del _td['body']
        mail.send(**_td)

        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual('someotheremail@somedomain.com', messages[0].to)

    def test_invalid_email_empty_sender(self):
        """Test that sending an invalid email (empty sender) raises the appropriate exception
        """
        _td = _test_data(sender='')
        with self.assertRaises(mail.InvalidEmailError):
            mail.send(**_td)

    def test_invalid_email_empty_to(self):
        """Test that sending an invalid email (empty to) raises the appropriate exception
        """
        _td = _test_data(to='')
        with self.assertRaises(mail.InvalidEmailError):
            mail.send(**_td)

    def test_invalid_no_sender(self):
        """Test that sending an invalid email (no sender) raises the appropriate exception
        """
        _td = _test_data()
        del _td['sender']
        with self.assertRaises(mail.MissingSenderError):
            mail.send(**_td)

    def test_invalid_no_to(self):
        """Test that sending an invalid email (no to) raises the appropriate exception
        """
        _td = _test_data()
        del _td['to']
        with self.assertRaises(mail.MissingRecipientsError):
            mail.send(**_td)

    def test_valid_email_async(self):
        """Test that sending a valid email asynchronously succeeds
        """
        mail.send_async(**_test_data())

        # check that mail hasn't been sent yet
        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(0, len(messages))

        # run the queued tasks and check they succeed
        for response in _run_tasks(self.taskq_stub, settings.EMAIL_QUEUE):
            self.assertEqual(response.status_int, 200)

        # check that mail was actually sent after the que's been run
        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(1, len(messages))
        self.assertEqual('someotheremail@somedomain.com', messages[0].to)
