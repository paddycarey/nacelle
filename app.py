"""
Simplest nacelle example possible
"""
# third-party imports
from webapp2 import Route

# local imports
from nacelle.core.decorators import render_jinja2


@render_jinja2('index.html')
def index(request):
    """Renders the index template with jinja2
    """
    return {'rendered_with': 'Jinja2'}



ROUTES = [
    Route(r'/', 'app.index', name='index'),
]
