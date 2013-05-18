"""
Nacelle project settings
"""
# slib imports
import os

# Convenience property to allow modules to quickly
# reference the project's root directory from anywhere
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# Set debug mode based on whether we're running locally or not
DEBUG = os.environ['SERVER_SOFTWARE'].startswith('Development')

# Extra WSGI config
WSGI_CONFIG = {
    'webapp2_extras.jinja2': {
        # list of directories to look in when loading templates
        'template_path': ['cms/templates', 'nacelle/templates'],
    },
    'webapp2_extras.sessions': {
        # secret key used for hashing session data, required
        # if you use nacelle's session capability
        'secret_key': None,
    }
}

# Details of sentry server for logging exceptions (set to None to disable)
SENTRY_DSN = None

CMS_CONFIG = {'models': [
    'demo_blog.models.post.Post',
    'demo_blog.models.category.Category',
    'cms.models.user.User',
]}
