"""
Simple set of example handlers for nacelle
"""
# marty mc fly imports
from __future__ import absolute_import

# local imports
from nacelle.core.decorators import render_handlebars
from nacelle.core.decorators import render_jinja2
from nacelle.core.decorators import render_json


@render_handlebars('index.html')
def hb_example(request):
    """Renders the index template with handlebars
    """
    return {'rendered_with': 'Handlebars'}


@render_jinja2('index.html')
def j2_example(request):
    """Renders the index template with jinja2
    """
    return {'rendered_with': 'Jinja2'}


@render_json
def json_example(request):
    """Renders the index template's context as JSON
    """
    return {'rendered_with': 'JSON'}
