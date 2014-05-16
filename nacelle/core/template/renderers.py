# third-party imports
import webapp2
from webapp2_extras import jinja2


def _get_jinja_renderer():
    """Get a jinja2 renderer, cached in the app registry
    """

    app = webapp2.get_app()
    return jinja2.get_jinja2(app=app)


def render_jinja2_template(template_name, context):
    """Renders a jinja2 template with the given context
    """

    renderer = _get_jinja_renderer()
    return renderer.render_template(template_name, **context)
