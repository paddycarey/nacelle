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



Request handlers
----------------

In nacelle/webapp2 vocabulary, `request handler` or simply `handler` is a common term that refers to the callable that contains the application logic to handle a request. This sounds very abstract, but we will explain everything in detail below.


Handlers 101
^^^^^^^^^^^^

A handler is equivalent to the `Controller` in the `MVC <http://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller>`_ terminology: in a simplified manner, it is where you process the request, manipulate data and define a response to be returned to the client: HTML, JSON, XML, files or whatever the app requires.

Normally a handler is a class that extends :class:`webapp2.RequestHandler` or, for compatibility purposes, ``webapp.RequestHandler``. Here is a simple one::

    class ProductHandler(webapp2.RequestHandler):
        def get(self, product_id):
            self.response.write('You requested product %r.' % product_id)


This code defines one request handler, ``ProductHandler``. When the application receives an HTTP request to a path the route for this handler, it instantiates the handler and calls the corresponding HTTP method from it. The handler above can only handle ``GET`` HTTP requests, as it only defines a ``get()`` method. To handle ``POST`` requests, it would need to implement a ``post()`` method, and so on.

The handler method receives a ``product_id`` extracted from the URI, and outputs a simple message containing the id as response. Not very useful, but this is just to show how it works. In a more complete example, the handler would fetch a corresponding record from a database and output an appropriate response -- HTML, JSON or XML with details about the requested product, for example.


HTTP methods translated to class methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The default behavior of the :class:`webapp2.RequestHandler` is to call a method that corresponds with the HTTP action of the request, such as the ``get()`` method for a HTTP GET request. The method processes the request and prepares a response, then returns. Finally, the application sends the response to the client.

The following example defines a request handler that responds to HTTP GET requests::

    class AddTwoNumbers(webapp2.RequestHandler):
        def get(self):
            try:
                first = int(self.request.get('first'))
                second = int(self.request.get('second'))

                self.response.write("<html><body><p>%d + %d = %d</p></body></html>" %
                                        (first, second, first + second))
            except (TypeError, ValueError):
                self.response.write("<html><body><p>Invalid inputs</p></body></html>")

A request handler can define any of the following methods to handle the
corresponding HTTP actions:

- ``get()``
- ``post()``
- ``head()``
- ``options()``
- ``put()``
- ``delete()``
- ``trace()``


View functions
^^^^^^^^^^^^^^

In some Python frameworks, handlers are called `view functions` or simply `views`. In Django, for example, `views` are normally simple functions that handle a request. Our examples use mostly classes, but nacelle handlers can also be normal functions equivalent to Django's `views`. nacelle currently encourages a functional style as most of its tools have been built to work with this style of handler, however, in future nacelle's tools should work with any type of handler.

A nacelle handler can, really, be **any** callable. The routing system has hooks to adapt how handlers are called, and two default adapters are used whether it is a function or a class. The following example demonstrates this::

    def display_product(request, *args, **kwargs):
        return webapp2.Response('You requested product %r.' % args[0])


Here, our handler is a simple function that receives the request instance, positional route variables as ``*args`` and named variables as ``**kwargs``, if they are defined.

Functions are an alternative for those that prefer their simplicity or think that handlers don't benefit that much from the power and flexibility provided by classes: inheritance, attributes, grouped methods, descriptors, metaclasses, etc. An app can have mixed handler classes and functions.

.. note::
   We avoid using the term `view` because it is often confused with the `View` definition from the classic `MVC` pattern. Django prefers to call its `MVC` implementation `MTV` (model-template-view), so `view` may make sense in their terminology. Still, we think that the term can cause unnecessary confusion and prefer to use `handler` instead, like in other Python frameworks (webapp, web.py or Tornado, for instance). In essence, though, they are synonyms.


Returned values
^^^^^^^^^^^^^^^

A handler method doesn't need to return anything: it can simply write to the response object using ``self.response.write()``.

But a handler **can** return values to be used in the response. Using the default dispatcher implementation, if a handler returns anything that is not ``None`` it **must** be a :class:`webapp2.Response` instance. If it does so, that response object is used instead of the default one.

For example, let's return a response object with a `Hello, world` message::

    class HelloHandler(webapp2.RequestHandler):
        def get(self):
            return webapp2.Response('Hello, world!')

This is the same as::

    class HelloHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('Hello, world!')


Overriding __init__()
^^^^^^^^^^^^^^^^^^^^^

If you want to override the :meth:`webapp2.RequestHandler.__init__` method, you must call :meth:`webapp2.RequestHandler.initialize` at the beginning of the method. It'll set the current request, response and app objects as attributes of the handler. For example::

    class MyHandler(webapp2.RequestHandler):
        def __init__(self, request, response):
            # Set self.request, self.response and self.app.
            self.initialize(request, response)

            # ... add your custom initializations here ...
            # ...
