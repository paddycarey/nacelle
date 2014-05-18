===========
URL Routing
===========

The URL router is the central part of a nacelle application, mapping incoming
URLs to the appropriate handlers.

nacelle uses a single central ``routes`` file to configure all URL mappings.
By default, nacelle looks for a ``ROUTES`` object (should be an iterable
containing ``webapp2.Route`` objects as in webapp2 itself) in the ``app``
module. This location can be configured using nacelle's ``settings.py`` as
such::

    # Python dotted path to the routes for the app
    ROUTES_MODULE = 'app.ROUTES'  # default routes module

For example, if your list of configured routes was defined as ``routes`` in
the ``apps.core.routes`` module, you could update your ``settings.py`` to
include the line::

    # Python dotted path to the routes for the app
    ROUTES_MODULE = 'apps.core.routes.routes'  # custom routes module

For the most part, **nacelle uses webapp2's routing infrastructure**, and you
should consult `those docs
<http://webapp-improved.appspot.com/guide/routing.html>`_ when you have any
questions or issues.


Multi-prefix routes
-------------------

The `webapp2_extras.routes
<http://webapp-improved.appspot.com/api/webapp2_extras/routes.html>`_ provides
several classes to wrap routes that share common characteristics:

- :mod:`webapp2_extras.routes.PathPrefixRoute`: receives a url path prefix
  and a list of routes that start with that prefix.
- :mod:`webapp2_extras.routes.HandlerPrefixRoute`: receives a handler module
  prefix in dotted notation and a list of routes that use that module.
- :mod:`webapp2_extras.routes.NamePrefixRoute`: receives a handler name
  prefix and a list of routes that start with that name.

The intention is to avoid repetition when defining routes. nacelle takes this
concept one step further and provides a single route class that allows
combining all three types of built-in ``PrefixRoute``.

For example, imagine we have these routes::

    from webapp2 import Route

    ROUTES = [
        Route('/users/<user:\w+>/', 'users.UserOverviewHandler', 'user-overview'),
        Route('/users/<user:\w+>/profile', 'users.UserProfileHandler', 'user-profile'),
        Route('/users/<user:\w+>/projects', 'users.UserProjectsHandler', 'user-projects'),
    ]

We could refactor them to use common prefixes::

    from nacelle.core.routes import MultiPrefixRoute
    from webapp2 import Route

    ROUTES = [
        MultiPrefixRoute(
            handler_pfx='users.',
            name_pfx='user-',
            path_pfx='/users/<user:\w+>',
            routes=[
                Route('/', 'UserOverviewHandler', 'overview'),
                Route('/profile', 'UserProfileHandler', 'profile'),
                Route('/projects', 'UserProjectsHandler', 'projects'),
            ],
        )
    ]

This is not only convenient, but also performs better: the nested routes
will only be tested if the path prefix matches.
