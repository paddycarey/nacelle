"""
A collection of useful custom validators for use with wtforms
"""
# stdlib imports
import imghdr
import base64

# third-party imports
from google.appengine.api import mail
from wtforms.validators import Required
from wtforms.validators import ValidationError


class RequiredIf(Required):

    """
    A validator which makes a field required if
    another field is set and has a truthy value
    """

    def __init__(self, other_field_name, other_field_values, *args, **kwargs):
        self.other_field_name = other_field_name
        self.other_field_values = other_field_values
        super(RequiredIf, self).__init__(*args, **kwargs)

    def __call__(self, form, field):
        other_field = form._fields.get(self.other_field_name)
        if other_field is None:
            raise Exception('no field named "%s" in form' % self.other_field_name)
        if other_field.data in self.other_field_values:
            super(RequiredIf, self).__call__(form, field)


def valid_image(form, field):

    """
    Validate a data url as an image
    """

    if field.data:

        try:
            image_data = field.data[5:].split(';', 1)[1].split(',', 1)[1]
            image_data = base64.b64decode(image_data)
        except (TypeError, IndexError):
            raise ValidationError("Invalid image detected (not valid base64)")

        image_valid = imghdr.what('dummy', image_data)
        if not image_valid:
            raise ValidationError("Invalid image detected")


def valid_sending_email(form, field):

    """
    Validate that we actually have permission to send mail from a given address
    """

    try:
        message = mail.EmailMessage()
        message.sender = field.data
        message.to = "photobooth-test@mailinator.com"
        message.subject = "Testing"
        message.body = "Testing"
        message.send()
    except mail.InvalidEmailError:
        raise ValidationError('Invalid email address detected')
    except mail.InvalidSenderError:
        raise ValidationError('Unauthorised email address detected')
