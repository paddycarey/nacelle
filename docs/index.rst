Welcome to nacelle's documentation!
======================================

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

nacelle is Free Software, released under the `MIT license
<http://opensource.org/licenses/MIT>`_.


Standing on the shoulders of giants
-----------------------------------

nacelle wouldn't be possible without the hard work of others and the fantastic
libraries upon which it builds. **If you have a problem with nacelle, and you
can't find the answer in these docs, you should try the documentation of
nacelle's components** by following the links below.

- `webapp2 <https://webapp-improved.appspot.com>`_:
    A lightweight Python web framework compatible with Google Appengine’s
    webapp. webapp2 is the main foundation for most of nacelle's WSGI/web
    functionality.
- `Jinja2 <http://jinja.pocoo.org/docs/>`_:
    A modern and designer friendly templating language for Python, modelled
    after Django’s templates. nacelle includes a preconfigured Jinja2
    environment ready for you to use.

This documentation won't try to cover absolutely everything, instead it aims
to cover only those bits of nacelle that differ significantly from webapp2,
pointing back to the original webapp2 docs where appropriate.


Contents
--------

.. toctree::
   :maxdepth: 2

   getting_started
   user_guide/index
   contributing
   authors
   history
