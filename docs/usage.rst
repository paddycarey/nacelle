=============
Using Nacelle
=============

At its core, nacelle provides a thin layer on top of webapp2, this is evident when you begin to build your applications. For the most part, when you encounter a problem, your first port of call should be the `webapp2 <http://webapp-improved.appspot.com/>`_ or `jinja2 <http://jinja.pocoo.org/docs/templates/>`_ documentation.

A nacelle app consists of 2 basic parts, routes and handlers. These are all that is required for a fully functioning nacelle application (a working example is included in the repository) but in practice you will likely require other components such as models, templates and utility classes/functions.


URI Routing
-----------


Simple Routing
^^^^^^^^^^^^^^

The simplest form of URI route in nacelle is a tuple ``(regex, handler)``, where `regex` is a regular expression to match the requested URI path and `handler` is a callable to handle the request. This routing mechanism is fully compatible with App Engine's webapp (and webapp2) framework.

Nacelle handlers can be any routable callable that returns a ``webapp2.Response``, this means that regular functions can be used as handlers in addition to webapp2's standard class-based handlers.

This is how it works: a list of routes is registered in the in the location specified by nacelle's settings (default ``routes.ROUTES``). When the application receives a request, it tries to match each one in order until one matches, and then call the corresponding handler. Here, for example, we define three handlers and register three routes that point to those handlers::

    ~/app.py

    from webapp2 import Response

    def index(request):
        return Response('Hello World!')

    class ProductHandler(webapp2.RequestHandler):
        def get(self, product_id):
            self.response.write('The product id is %s' % product_id)


    ~/routes.py

    ROUTES = [
        (r'/', 'app.index'),
        (r'/products/(\d+)', 'app.ProductHandler'),
    ])

When a request comes in, the application will match the request path to find the corresponding handler. If no route matches, an ``HTTPException`` is raised with status code 404, and your application can handle it accordingly.

The `regex` part is an ordinary regular expression (see the :py:mod:`re` module) that can define groups inside parentheses. The matched group values are passed to the handler as positional arguments. In the example above, the last route defines a group, so the handler will receive the matched value when the route matches (one or more digits in this case).

The `handler` part can be a direct reference to an imported module i.e. ``(r'/', somemodule.SomeHandler)`` but it can also be a string in dotted notation to be lazily imported when needed if you prefer.

Simple routes are easy to use and enough for a lot of cases but don't support keyword arguments, URI building, domain and subdomain matching, automatic redirection and other useful features. For this, nacelle offers the extended routing mechanism that we'll see next.


Extended routes
^^^^^^^^^^^^^^^

nacelle introduces a routing mechanism that extends the webapp model to provide additional features:

- **URI building:** the registered routes can be built when needed, avoiding hardcoded URIs in the app code and templates. If you change the route definition in a compatible way during development, all places that use that route will continue to point to the correct URI. This is less error prone and easier to maintain.
- **Keyword arguments:** handlers can receive keyword arguments from the matched URIs. This is easier to use and also more maintanable than positional arguments.
- **Nested routes:** routes can be extended to match more than the request path. We will see below a route class that can also match domains and subdomains.

And several other features and benefits.

The concept is similar to the simple routes we saw before, but instead of a
tuple ``(regex, handler)``, we define each route using the class
:class:`webapp2.Route`. Let's remake our previous routes using it::

    ROUTES = [
        webapp2.Route(r'/', handler='app.index', name='index'),
        webapp2.Route(r'/products/<product_id:\d+>', handler='app.ProductHandler', name='product'),
    ]

The first argument in the routes above is a :ref:`URL template`, the `handler` argument is the :ref:`request handler` to be used, and the `name` argument is a name used to build a URI for that route.


The URL template
^^^^^^^^^^^^^^^^

The URL template defines the URL path to be matched. It can have regular expressions for variables using the syntax ``<name:regex>``; everything outside of ``<>`` is not interpreted as a regular expression to be matched. Both name and regex are optional, like in the examples below:

=================  ==================================
Format             Example
=================  ==================================
``<name>``         ``'/blog/<year>/<month>'``
``<:regex>``       ``'/blog/<:\d{4}>/<:\d{2}>'``
``<name:regex>``   ``'/blog/<year:\d{4}>/<month:\d{2}>'``
=================  ==================================

The same template can mix parts with name, regular expression or both.

The name, if defined, is used to build URLs for the route. When it is set, the value of the matched regular expression is passed as keyword argument to the handler. Otherwise it is passed as a positional argument.

If only the name is set, it will match anything except a slash. So these routes are equivalent::

    Route('/<user_id>/settings', handler=SettingsHandler, name='user-settings')
    Route('/<user_id:[^/]+>/settings', handler=SettingsHandler, name='user-settings')

.. note::
   The handler only receives ``*args`` if no named variables are set. Otherwise, the handler only receives ``**kwargs``. This allows you to set regular expressions that are not captured: just mix named and unnamed variables and the handler will only receive the named ones.


Advanced Routing
^^^^^^^^^^^^^^^^

Please see the `webapp2 <http://webapp-improved.appspot.com/>`_ documentation for more advanced routing techniques.
