nacelle microframework
======================

[![Build Status](https://travis-ci.org/rehabstudio/nacelle.png?branch=master)](https://travis-ci.org/rehabstudio/nacelle)
[![Coverage Status](https://coveralls.io/repos/rehabstudio/nacelle/badge.png)](https://coveralls.io/r/rehabstudio/nacelle)

A lightweight microframework built on top of webapp2 for use on Google Appengine

<strong>NOTE:</strong> Before reading any further, if you need portability from appengine or a relational database then nacelle probably isn't for you, use CloudSQL and Django, you'll thank me later.

nacelle aims to provide a small but solid set of tools that enable developers to quickly get a new app up and running, whilst not sacrificing any of the flexibility and power of webapp2 in the process. nacelle is suitable for building both tiny prototypes and large complex applications, it should never get in your way.


Get started
===========

1. Download the latest version of the [App Engine SDK](http://code.google.com/appengine/downloads.html#Google_App_Engine_SDK_for_Python) for Linux, Mac OS or Windows
2. Download the latest version of [nacelle](https://github.com/paddycarey/nacelle/archive/master.zip)
3. Unpack nacelle into a new directory and switch to it
4. Run! `dev_appserver.py .`
5. See! [http://localhost:8080](http://localhost:8080)


Functions and Features
======================

- Authentication using Appengine's built-in users service
- Custom testrunner to help with loading the appengine environment for nose
- Error handling (with logging to a sentry server)
- Session management and automatic secret key generation
- Template rendering (with Jinja2 or Handlebars)
- Easily run tasks in the background outside of the request loop


Thanks!
=======

The following libraries are included by default:

- [webapp2](http://webapp-improved.appspot.com/)
- [jinja2](http://jinja.pocoo.org/docs/)
- [raven](https://github.com/getsentry/raven-python)
- [pybars](https://launchpad.net/pybars)
- [pymeta](https://launchpad.net/pymeta)


License
=======

nacelle is licensed under the MIT license.


Sorry
=====

On one final note, I've been pretty atrocious at maintaining any semblance of backwards compatibility in nacelle since its inception, that needs to change. As nacelle begins to stabilise and approach a 1.0 release, the public API should also begin to settle down. Following a 1.0 release nacelle will follow a semantic versioning scheme to help identify releases with major, breaking changes.

For now though, you've been warned.
