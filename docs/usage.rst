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


Request data
------------

The request handler instance can access the request data using its ``request`` property. This is initialized to a populated `WebOb`_ ``Request`` object by the application.

The request object provides a ``get()`` method that returns values for arguments parsed from the query and from POST data. The method takes the argument name as its first parameter. For example::

    class MyHandler(webapp2.RequestHandler):
        def post(self):
            name = self.request.get('name')

or::

    def my_handler(request):
        name = request.get('name')

By default, ``get()`` returns the empty string (``''``) if the requested argument is not in the request. If the parameter ``default_value`` is specified, ``get()`` returns the value of that parameter instead of the empty string if the argument is not present.

If the argument appears more than once in a request, by default ``get()`` returns the first occurrence. To get all occurrences of an argument that might appear more than once as a list (possibly empty), give ``get()`` the argument ``allow_multiple=True``::

    # <input name="name" type="text" />
    name = request.get("name")

    # <input name="subscribe" type="checkbox" value="yes" />
    subscribe_to_newsletter = request.get("subscribe", default_value="no")

    # <select name="favorite_foods" multiple="true">...</select>
    favorite_foods = request.get("favorite_foods", allow_multiple=True)

    # for food in favorite_foods:
    # ...

For requests with body content that is not a set of CGI parameters, such as the body of an HTTP PUT request, the request object provides the attributes ``body`` and ``body_file``: ``body`` is the body content as a byte string and ``body_file`` provides a file-like interface to the same data::

    uploaded_file = request.body


GET data
^^^^^^^^

Query string variables are available in ``request.GET``.

``.GET`` is a `MultiDict`_: it is like a dictionary but the same key can have multiple values. When you call ``.get(key)`` for a key with multiple values, the last value is returned. To get all values for a key, use ``.getall(key)``. Examples::

    request = Request.blank('/test?check=a&check=b&name=Bob')

    # The whole MultiDict:
    # GET([('check', 'a'), ('check', 'b'), ('name', 'Bob')])
    get_values = request.GET

    # The last value for a key: 'b'
    check_value = request.GET['check']

    # All values for a key: ['a', 'b']
    check_values = request.GET.getall('check')

    # An iterable with alll items in the MultiDict:
    # [('check', 'a'), ('check', 'b'), ('name', 'Bob')]
    request.GET.items()

The name ``GET`` is a bit misleading, but has historical reasons: ``request.GET`` is not only available when the HTTP method is GET. It is available for any request with query strings in the URI, for any HTTP method: GET, POST, PUT etc.


POST data
^^^^^^^^^

Variables url encoded in the body of a request (generally a POST form submitted using the ``application/x-www-form-urlencoded`` media type) are available in ``request.POST``.

It is also a `MultiDict`_ and can be accessed in the same way as ``.GET``. Examples::

    request = Request.blank('/')
    request.method = 'POST'
    request.body = 'check=a&check=b&name=Bob'

    # The whole MultiDict:
    # POST([('check', 'a'), ('check', 'b'), ('name', 'Bob')])
    post_values = request.POST

    # The last value for a key: 'b'
    check_value = request.POST['check']

    # All values for a key: ['a', 'b']
    check_values = request.POST.getall('check')

    # An iterable with alll items in the MultiDict:
    # [('check', 'a'), ('check', 'b'), ('name', 'Bob')]
    request.POST.items()

Like ``GET``, the name ``POST`` is a somewjat misleading, but has historical reasons: they are also available when the HTTP method is PUT, and not only POST.


GET + POST data
^^^^^^^^^^^^^^^

``request.params`` combines the variables from ``GET`` and ``POST``. It can be used when you don't care where the variable comes from.


Files
^^^^^

Uploaded files are available as ``cgi.FieldStorage`` (see the :py:mod:`cgi` module) instances directly in ``request.POST``.


Cookies
^^^^^^^

Cookies can be accessed in ``request.cookies``. It is a simple dictionary::

    request = Request.blank('/')
    request.headers['Cookie'] = 'test=value'

    # A value: 'value'
    cookie_value = request.cookies.get('test')


Common Request attributes
^^^^^^^^^^^^^^^^^^^^^^^^^

body
  A file-like object that gives the body of the request.
content_type
  Content-type of the request body.
method
  The HTTP method, e.g., 'GET' or 'POST'.
url
  Full URI, e.g., ``'http://localhost/blog/article?id=1'``.
scheme
  URI scheme, e.g., 'http' or 'https'.
host
  URI host, e.g., ``'localhost:80'``.
host_url
  URI host including scheme, e.g., ``'http://localhost'``.
path_url
  URI host including scheme and path, e.g., ``'http://localhost/blog/article'``.
path
  URI path, e.g., ``'/blog/article'``.
path_qs
  URI path including the query string, e.g., ``'/blog/article?id=1'``.
query_string
  Query string, e.g., ``id=1``.
headers
  A dictionary like object with request headers. Keys are case-insensitive.
GET
  A dictionary-like object with variables from the query string, as unicode.
POST
  A dictionary-like object with variables from a POST form, as unicode.
params
  A dictionary-like object combining the variables GET and POST.
cookies
  A dictionary-like object with cookie values.


Extra attributes
^^^^^^^^^^^^^^^^

The parameters from the matched :class:`webapp2.Route` are set as attributes of the request object. They are ``request.route_args``, for positional arguments, and ``request.route_kwargs``, for keyword arguments. The matched route object is available as ``request.route``.

A reference to the active WSGI application is also set as an attribute of the request. You can access it in ``request.app``.


Getting the current request
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The active ``Request`` instance can be accessed during a request using the function :func:`webapp2.get_request`.


Registry
^^^^^^^^

A simple dictionary is available in the request object to register instances that are shared during a request: it is the :attr:`webapp2.Request.registry` attribute.

A registry dictionary is also available in the :ref:`WSGI application object <guide.app.registry>`, to store objects shared across requests.


Learn more about WebOb
^^^^^^^^^^^^^^^^^^^^^^

WebOb is an open source third-party library. See the `WebOb`_ documentation for a detailed API reference and examples.


.. _WebOb: http://docs.webob.org/
.. _MultiDict: http://pythonpaste.org/webob/class-webob.multidict.MultiDict.html


Building a Response
^^^^^^^^^^^^^^^^^^^

The class based request handler instance builds the response using its response property. This is initialized to an empty `WebOb`_ ``Response`` object by the application.

The response object acts as a file-like object that can be used for writing the body of the response::

    class MyHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write("<html><body><p>Hi there!</p></body></html>")

The response buffers all output in memory, then sends the final output when the handler exits. webapp2 does not support streaming data to the client.

The ``clear()`` method erases the contents of the output buffer, leaving it empty.

If the data written to the output stream is a Unicode value, or if the response includes a ``Content-Type`` header that ends with ``; charset=utf-8``, webapp2 encodes the output as UTF-8. By default, the ``Content-Type`` header is ``text/html; charset=utf-8``, including the encoding behavior. If the ``Content-Type`` is changed to have a different charset, webapp2 assumes the output is a byte string to be sent verbatim.

.. warning:
   The ``status`` attribute from a response is the status code plus message, e.g., '200 OK'. This is different from webapp, which has the status code (an integer) stored in ``status``. In webapp2, the status code is stored in the ``status_int`` attribute, as in WebOb.


Setting cookies
^^^^^^^^^^^^^^^

Cookies are set in the response object. The methods to handle cookies are:

set_cookie(key, value='', max_age=None, path='/', domain=None, secure=None, httponly=False, comment=None, expires=None, overwrite=False)
  Sets a cookie.

delete_cookie(key, path='/', domain=None)
  Deletes a cookie previously set in the client.

unset_cookie(key)
  Unsets a cookie previously set in the response object. Note that this doesn't delete the cookie from clients, only from the response.

For example::

    # Saves a cookie in the client.
    response.set_cookie('some_key', 'value', max_age=360, path='/',
                        domain='example.org', secure=True)

    # Deletes a cookie previously set in the client.
    response.delete_cookie('bad_cookie')

    # Cancels a cookie previously set in the response.
    response.unset_cookie('some_key')

Only the ``key`` parameter is required. The parameters are:

key
  Cookie name.
value
  Cookie value.
expires
  An expiration date. Must be a :py:mod:`datetime`.datetime object. Use this
  instead of max_age since the former is not supported by Internet Explorer.
max_age
  Cookie max age in seconds.
path
  URI path in which the cookie is valid.
domain
  URI domain in which the cookie is valid.
secure
  If True, the cookie is only available via HTTPS.
httponly
  Disallow JavaScript to access the cookie.
comment
  Defines a cookie comment.
overwrite
  If true, overwrites previously set (and not yet sent to the client) cookies
  with the same name.


Common Response attributes
^^^^^^^^^^^^^^^^^^^^^^^^^^

status
  Status code plus message, e.g., '404 Not Found'. The status can be set passing an ``int``, e.g., ``request.status = 404``, or including the message, e.g., ``request.status = '404 Not Found'``.
status_int
  Status code as an ``int``, e.g., 404.
status_message
  Status message, e.g., 'Not Found'.
body
  The contents of the response, as a string.
unicode_body
  The contents of the response, as a unicode.
headers
  A dictionary-like object with headers. Keys are case-insensitive. It supports multiple values for a key, but you must use ``response.headers.add(key, value)`` to add keys. To get all values, use ``response.headers.getall(key)``.
headerlist
  List of headers, as a list of tuples ``(header_name, value)``.
charset
  Character encoding.
content_type
  'Content-Type' value from the headers, e.g., ``'text/html'``.
content_type_params
  Dictionary of extra Content-type parameters, e.g., ``{'charset': 'utf8'}``.
location
  'Location' header variable, used for redirects.
etag
  'ETag' header variable. You can automatically generate an etag based on the response body calling ``response.md5_etag()``.


Response Decorators
^^^^^^^^^^^^^^^^^^^

When using functional style decorators in Nacelle it is not necessary to explicitly build and return response objects in most common cases. Nacelle includes several decorators that make returning specific types of response very easy.

The ``render_json`` decorator allows a handler function to return any python dictionary and have it automatically serialised to JSON in the response body. This decorator will also set the appropriate ``content-type`` header in the response::

    from nacelle.core.decorators import render_json

    @render_json
    def my_handler(request):
        return {'somekey': 1, 'someotherkey': 2, 'somelist': [0, 1, 2, 3, 4]}

The ``render_handlebars`` and ``render_jinja2`` decorators allow easy rendering to template, either using Handlebars or Jinja2 (see `Rendering Templates` section for full details). Both decorators take a single argument, the name of the template used to render the response. Nacelle includes a ``templates/`` directory in the root of the application by default, templates should be stored in this folder for easy access::

    from nacelle.core.decorators import render_handlebars
    from nacelle.core.decorators import render_jinja2

    @render_handlebars('sometemplate.html')
    def my_handler(request):
        context = {'somekey': 'somedata'}

    @render_jinja2('somedir/sometemplate.html')
    def my_other_handler(request):
        context = {'somekey': 'somedata'}
