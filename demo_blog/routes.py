# third-party imports
from webapp2 import Route
from webapp2_extras.routes import RedirectRoute


ROUTES = [

    # Blog Index page
    Route(
        r'/',
        'demo_blog.handlers.BlogHandler',
        name='blog-index'
    ),

    # Individual blog post
    RedirectRoute(
        r'/<post_id:\d+>/.?*',
        'demo_blog.handlers.BlogHandler',
        strict_slash=True,
        name='blog-post'
    ),

]

# EXTRA_CMS_ROUTES = [

#     RedirectRoute(
#         r'/publish/<key>/',
#         factory.delete_handler(model),
#         name="cms-%s-%s-delete" % (app_name, model_name),
#         strict_slash=True
#     ),

# ]
