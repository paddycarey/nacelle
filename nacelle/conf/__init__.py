# marty mcfly imports
from __future__ import absolute_import

# stdlib imports
import webapp2


class Settings(object):

    def __init__(self):
        try:
            self._user_settings = webapp2.import_string('settings')
        except webapp2.ImportStringError:
            self._user_settings = None
        self._default_settings = webapp2.import_string('nacelle.conf.default_settings')

    def __getattr__(self, name):

        try:
            return getattr(self._user_settings, name)
        except AttributeError:
            pass
        try:
            return getattr(self._default_settings, name)
        except AttributeError:
            pass
        raise AttributeError('setting not found: %s' % name)

# init our settings object
settings = Settings()
