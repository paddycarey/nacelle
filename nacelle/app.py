# stdlib imports
import os
import sys

# third-party imports
import webapp2

# local imports
import settings

# Add lib directory to path
sys.path.insert(0, os.path.join(settings.PROJECT_ROOT, 'nacelle', 'lib'))

import routes

# Define our WSGI app so GAE can run it
wsgi = webapp2.WSGIApplication(
    routes.ROUTES,
    debug=settings.DEBUG,
    config=settings.WSGI_CONFIG
)
