"""
Simple model that stores the secret key used to hash our sessions
"""
# third-party imports
from google.appengine.ext import ndb

# local imports
from nacelle.core.utils.crypto import get_random_string


class DummyKey(object):
    pass


class SecretKey(ndb.Model):

    created = ndb.DateTimeProperty(auto_now_add=True, indexed=False)
    modified = ndb.DateTimeProperty(auto_now=True, indexed=False)
    secret_key = ndb.StringProperty(required=True, indexed=False)

    @classmethod
    def get_key(cls):
        # Create a random NACELLE_SECRET_KEY
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        generated_key = get_random_string(50, chars)
        # get or insert the secret key in the datastore
        try:
            entity = cls.get_or_insert('NACELLE_SECRET_KEY', secret_key=generated_key)
        except AssertionError:
            # catch error thrown because of lack of memcache stub when testing, this is entirely for convenience
            entity = DummyKey()
            entity.secret_key = generated_key
        secret_key = entity.secret_key
        return str(secret_key)
