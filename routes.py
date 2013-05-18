"""
Nacelle routes module

All URLs should be defined directly in this module, or if you prefer, defined
elsewhere and imported here.  Either way, all of your routes need to end up
here so Nacelle can pick them up.
"""
# third-party imports
from webapp2 import Route
from webapp2_extras.routes import PathPrefixRoute
from webapp2_extras.routes import RedirectRoute

# local imports
from cms.routes import build as cms_routes
from demo_blog.routes import ROUTES as demo_blog_routes

ROUTES = [

    ####################
    # Admin/CMS Routes #
    ####################

    # Simple redirect routes to catch '/' and '/admin' and redirect into the CMS
    RedirectRoute(r'/admin', redirect_to_name='cms-index'),
    # Catch all CMS routes with /admin prefix
    PathPrefixRoute('/admin', cms_routes.build_routes()),

    ###################
    # Frontend routes #
    ###################

    Route(r'/', 'nacelle.handlers.default.DefaultIndexHandler', name='index'),

    ####################
    # Demo Blog Routes #
    ####################

    # Simple redirect routes to catch '/' and '/admin' and redirect into the CMS
    RedirectRoute(r'/blog', redirect_to_name='blog-index'),
    # Catch all CMS routes with /admin prefix
    PathPrefixRoute('/blog', demo_blog_routes),

]
