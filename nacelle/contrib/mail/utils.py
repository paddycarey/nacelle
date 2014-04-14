"""Utilities used to render and send emails
"""
# marty mcfly imports
from __future__ import absolute_import
from __future__ import unicode_literals

from nacelle.core.template.renderers import render_jinja2_template


def render_email(template, context=None):
    """Uses Jinja2 to render the email
    """
    if context is None:
        context = {}
    email_body = render_jinja2_template(template, context)
    return email_body
