"""Utilities used to send emails
"""
# marty mcfly imports
from __future__ import absolute_import

# third-party imports
from google.appengine.api import mail
from google.appengine.api import taskqueue
from nacelle.conf import settings


def _construct_and_validate(**kwargs):
    """Constructs and validates an EmailMessage object before sending
    """
    msg = mail.EmailMessage(**kwargs)
    msg.check_initialized()
    return msg


def send(**kwargs):
    """Sends an email using appengine's mail service

    This function accepts the same arguments as appengine's mail.send_mail()
    """
    msg = _construct_and_validate(**kwargs)
    msg.send()


def send_async(**kwargs):
    """Enqueues a job to send an email using appengine's taskqueue

    It's safer to do this on a task queue since we can automatically retry if
    we start to hit errors at high volume (or for any other reason.

    This function accepts the same arguments as appengine's mail.send_mail()
    """
    _construct_and_validate(**kwargs)
    taskqueue.add(
        url='/_ah/send_email/',
        params=kwargs,
        queue_name=settings.EMAIL_QUEUE,
    )
