# stdlib imports
from collections import OrderedDict

# third-party imports
import webapp2
from webapp2 import Route
from webapp2_extras.routes import PathPrefixRoute
from webapp2_extras.routes import RedirectRoute

# local imports
from cms.handlers import factory
from settings import CMS_CONFIG


def build_routes_for_model(model, app_name, model_name):

    route = PathPrefixRoute('/%s/%s' % (app_name, model_name), [
        RedirectRoute(
            r'/',
            factory.list_handler(model),
            name="cms-%s-%s-list" % (app_name, model_name),
            strict_slash=True
        ),
        RedirectRoute(
            r'/rows',
            factory.row_handler(model),
            name="cms-%s-%s-rows" % (app_name, model_name),
            strict_slash=True
        ),
        RedirectRoute(
            r'/edit/',
            factory.form_handler(model),
            name="cms-%s-%s-new" % (app_name, model_name),
            handler_method='handle',
            strict_slash=True
        ),
        RedirectRoute(
            r'/edit/<key>/',
            factory.form_handler(model),
            name="cms-%s-%s-edit" % (app_name, model_name),
            handler_method='handle',
            strict_slash=True
        ),
        RedirectRoute(
            r'/delete/<key>/',
            factory.delete_handler(model),
            name="cms-%s-%s-delete" % (app_name, model_name),
            strict_slash=True
        ),
        RedirectRoute(
            r'/<action>/',
            factory.bulk_action_handler(model),
            name="cms-%s-%s-bulk-action" % (app_name, model_name),
            strict_slash=True
        ),
    ])
    return route


def build_routes():

    """
    Build and return routes for a given model
    """

    try:
        index_handler = CMS_CONFIG['index_handler']
    except KeyError:
        index_handler = 'cms.handlers.index.IndexHandler'

    routes = [

        # CMS Index page
        Route(
            r'/',
            index_handler,
            name='cms-index'
        ),

        # Edit user settings
        RedirectRoute(
            r'/login/',
            'cms.handlers.login.LoginHandler',
            strict_slash=True,
            name='cms-login'
        ),

    ]
    for model_string in CMS_CONFIG['models']:
        model = webapp2.import_string(model_string)
        app_name = model_string.split(".")[0].lower()
        model_name = model_string.split(".")[-1].lower()
        routes.append(build_routes_for_model(model, app_name, model_name))
    return routes


def get_nav():

    app = webapp2.get_app()
    # Check if the instance is already registered.
    cms_nav = app.registry.get('cms_nav')
    if not cms_nav:

        cms_nav = OrderedDict()
        for model_string in CMS_CONFIG['models']:
            model = webapp2.import_string(model_string)
            app_name = model_string.split(".")[0].lower()
            model_name = model_string.split(".")[-1].lower()
            nav_stub = {
                'url': "cms-%s-%s-list" % (app_name, model_name),
                'icon': model.Meta.header_icon,
                'label': model.Meta.header_title or 'Manage %ss' % model_name
            }
            if app_name in cms_nav:
                cms_nav[app_name].append(nav_stub)
            else:
                cms_nav[app_name] = [nav_stub]

        # Register the instance in the registry.
        app.registry['cms_nav'] = cms_nav

    return cms_nav
