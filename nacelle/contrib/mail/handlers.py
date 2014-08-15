"""Mail related request handlers
"""
# marty mcfly imports
from __future__ import absolute_import

# third-party imports
from nacelle.core.decorators import login_task
from nacelle.core.decorators import render_json

# local imports
from .interface import send


@render_json
@login_task
def send_email(request):
    """Sends emails asynchronously on a taskqueue
    """
    # send emails and return some manner of success response
    send(**request.params)
    return {'success': 'mail sent!'}
