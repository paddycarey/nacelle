"""Routes that facilitate the sending of emails.
"""
# third-party imports
from webapp2 import Route


ROUTES = [
    # Route to allow sending mail on a taskqueue in the background
    Route(r'/_ah/send_email/', 'nacelle.contrib.mail.handlers.send_email', name='nacelle-task-send-email'),
]
