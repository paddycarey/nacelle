"""
A collection of useful custom widgets for use with wtforms
"""
# stdlib imports
from cgi import escape

# third-party imports
import jinja2
from wtforms.compat import text_type
from wtforms.widgets import html_params
from wtforms.widgets import HTMLString
from wtforms.widgets import Input

# init a stripped down template env so we can load any required widget templates
template_env = jinja2.Environment(loader=jinja2.FileSystemLoader('nacelle/templates'))


class ImageWidget(Input):
    """
    Renders a file field with instant image preview
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        image_widget_template = template_env.get_template('cms/forms/widgets/image.html')
        return HTMLString(image_widget_template.render(name=field.name, max_width=field.max_width, max_height=field.max_height, **kwargs))


class RichTextWidget(object):
    """
    Renders a multi-line text area.

    `rows` and `cols` ought to be passed as keyword args when rendering.
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        return HTMLString('<textarea class="form-rich-text" %s>%s</textarea>' % (html_params(name=field.name, **kwargs), escape(text_type(field._value()))))


class DateWidget(Input):
    """
    Renders a datepicker widget
    """
    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        if 'value' not in kwargs:
            kwargs['value'] = field._value()
        date_widget_template = template_env.get_template('cms/forms/widgets/date.html')
        return HTMLString(date_widget_template.render(name=field.name, **kwargs))
