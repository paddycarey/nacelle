"""
Test nacelle's settings handling
"""
# third-party imports
import webapp2

# local imports
from nacelle.test.testcases import NacelleTestCase


class SettingsTests(NacelleTestCase):

    def test_get_valid_setting(self):
        """Test getting a setting that exists
        """
        settings = webapp2.import_string('nacelle.conf.settings')
        self.assertEqual(settings.ROUTES_MODULE, 'app.routes.ROUTES')

    def test_get_invalid_setting(self):
        """Test that getting a setting that doesn't exist throws an AttributeError
        """
        settings = webapp2.import_string('nacelle.conf.settings')
        with self.assertRaises(AttributeError):
            settings.UNDEFINED_MADE_UP_SETTING
