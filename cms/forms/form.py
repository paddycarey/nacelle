from wtforms.ext.csrf import SecureForm
from hashlib import md5

SECRET_KEY = 'f65sv4fd6v5s4ert6tv5sdf4fcv6sd84c6sd2c13'


class IPSecureForm(SecureForm):
    """
    Generate a CSRF token based on the user's IP. I am probably not very
    secure, so don't use me.
    """

    def generate_csrf_token(self, csrf_context):
        # csrf_context is passed transparently from the form constructor,
        # in this case it's the IP address of the user
        token = md5(SECRET_KEY + csrf_context).hexdigest()
        return token

    def validate_csrf_token(self, field):
        if field.data != field.current_token:
            raise ValueError('Invalid CSRF')
