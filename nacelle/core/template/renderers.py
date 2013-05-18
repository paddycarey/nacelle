# third-party imports
import logging
import webapp2
from webapp2_extras import jinja2

# local imports
from nacelle.core.template.loaders import load_handlebars_template


def _get_handlebars_compiler():
    """
    Get an instance of a handlebars compiler, from the app registry of
    instantiating when required.
    """

    app = webapp2.get_app()
    # Check if the instance is already registered.
    compiler = app.registry.get('handlebars_compiler')
    if not compiler:
        logging.info('Compiler not cached, loading')
        compiler = webapp2.import_string('pybars.Compiler')()
        # Register the instance in the registry.
        app.registry['handlebars_compiler'] = compiler
    return compiler


def _compile_handlebars_template(template_name):
    """
    Compile and cache a handlebars template in the app registry
    """

    app = webapp2.get_app()
    # Check if the instance is already registered.
    compiled_template = app.registry.get('compiled-template-%s' % template_name)
    if not compiled_template:
        template_string = load_handlebars_template(template_name)
        compiler = _get_handlebars_compiler()
        logging.info('Template not cached, compiling: %s' % template_name)
        compiled_template = compiler.compile(template_string)
        # Register the instance in the registry.
        app.registry['compiled-template-%s' % template_name] = compiled_template
    return compiled_template


def _get_jinja_renderer():
    """Get a jinja2 renderer, cached in the app registry
    """

    app = webapp2.get_app()
    return jinja2.get_jinja2(app=app)


def render_handlebars_template(template_name, context):
    """Renders a handlebars template with the given context
    """

    compiled_template = _compile_handlebars_template(template_name)
    output = compiled_template(context)
    return unicode(output)


def render_jinja2_template(template_name, context):
    """Renders a jinja2 template with the given context
    """

    renderer = _get_jinja_renderer()
    return renderer.render_template(template_name, **context)
