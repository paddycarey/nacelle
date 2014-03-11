# Nacelle Microframework

![Appengine](http://i.imgur.com/9N2DNQn.png)

A lightweight python microframework built on top of webapp2 for use on Google Appengine


## Overview

Nacelle aims to provide a small but solid set of tools that enable developers to quickly get a new app up and running, whilst not sacrificing any of the flexibility and power of webapp2 in the process. Nacelle is suitable for building everything from tiny prototypes to large complex applications, it should never get in your way.

**Nacelle is free software released under the [MIT License](http://opensource.org/licenses/MIT)**


## Features

- Authentication using Appengine's built-in users service
- Custom testrunner to help with loading the appengine environment for nose
- Error handling (with optional logging to a sentry server)
- Session management and automatic secret key generation
- Template rendering (with Jinja2 or Handlebars)
- Easily run tasks in the background outside of the request loop


## Sorry

On one final note, I've been pretty atrocious at maintaining any semblance of backwards compatibility in nacelle since its inception, that needs to change. As nacelle begins to stabilise and approach a 1.0 release, the public API should also begin to settle down. Following a 1.0 release nacelle will follow a semantic versioning scheme to help identify releases with major, breaking changes.

For now though, you've been warned.
