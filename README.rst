===============================
Nacelle Microframework
===============================

.. image:: https://travis-ci.org/nacelle/nacelle.png?branch=master
        :target: https://travis-ci.org/nacelle/nacelle

.. image:: https://coveralls.io/repos/rehabstudio/nacelle/badge.png
        :target: https://coveralls.io/r/rehabstudio/nacelle

.. image:: https://badge.fury.io/py/nacelle.png
    :target: http://badge.fury.io/py/nacelle

nacelle is a lightweight Python web framework, built on top of webapp2,
designed for use on Google Appengine.

nacelle aims to provide a small but solid set of tools that enable developers
to quickly get a new app up and running, whilst not sacrificing any of the
flexibility and power of webapp2 in the process. Nacelle is suitable for
building everything from tiny prototypes to large complex applications, it
should never get in your way.

.. note::
    If you need portability from appengine then nacelle probably isn't for you,
    use Django, Flask or one of the many other awesome Python web frameworks
    that exist, you'll thank me later.

* Free software: `MIT license <http://opensource.org/licenses/MIT>`_
* Documentation: http://nacelle.rtfd.org.


Features
--------

* Authentication using Appengine's built-in users service
* Custom testrunner to help with loading the appengine environment for nose
* Error handling (with optional logging to a sentry server)
* Session management and automatic secret key generation
* Template rendering (with Jinja2 or Handlebars)
* Easily run tasks in the background outside of the request loop
