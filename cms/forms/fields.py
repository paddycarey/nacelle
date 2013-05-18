"""
A collection of useful custom fields for use with wtforms
"""
# third-party imports
from wtforms import fields
from wtforms.compat import text_type

# local imports
from cms.forms import widgets
from cms.forms.validators import valid_image


class ImageField(fields.TextField):

    """
    Convert images to and from base64 for easy storage
    """

    widget = widgets.ImageWidget()

    def __init__(self, label='', validators=None, max_width=200, max_height=200, **kwargs):
        if validators is None:
            validators = [valid_image]
        super(ImageField, self).__init__(label, validators, **kwargs)
        self.max_width = max_width
        self.max_height = max_height


class RichTextField(fields.TextAreaField):

    """
    Render a rich text editor in a form using CKEditor
    """

    widget = widgets.RichTextWidget()


class StringListField(fields.TextField):

    """
    List items are rendered in a comma seperated list.
    """

    def _value(self):
        if self.raw_data:
            return self.raw_data[0]
        else:
            return self.data and text_type(",".join(self.data)) or ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = valuelist[0].lstrip(',').split(',')
            except ValueError:
                raise ValueError(self.gettext('Not a valid list'))


class DateField(fields.DateField):

    widget = widgets.DateWidget()
