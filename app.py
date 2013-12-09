"""
Simplest nacelle example possible
"""
# local imports
from nacelle.core.decorators import render_jinja2


@render_jinja2('index.html')
def index(request):
    """Renders the index template with jinja2
    """
    return {'rendered_with': 'Jinja2'}
