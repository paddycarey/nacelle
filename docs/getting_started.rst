===============
Getting Started
===============

nacelle depends on a few external external libraries for operation, however,
we have a policy that nacelle core should never have a hard dependency on any
library which is not available with the Google Appengine Python SDK, therefore
getting started is easy.

You'll first need to install the `App Engine Python SDK`_. See the README file
for directions. You’ll need python 2.7 and `pip`_ 1.4 or later installed too.

Appengine requires that all external libraries being used should be included
(vendored) into the application directory itself. Different developers have
their own methods for dealing with this issue, and nacelle should work
perfectly fine with whatever your preferred application structure is (if it
doesn't, let us know). This article covers one such method, aiming to provide
a quick overview of what it takes to get started with nacelle.


New Project Skeleton
--------------------

The nacelle project provides a barebones skeleton you can use to get your
application off the ground quickly. You should clone the skeleton's git
repository to a convenient location::

    $ git clone https://github.com/nacelle/nacelle-skeleton.git your-project-name

Once cloned, you should use `pip`_ to install the latest version of nacelle
into the application's ``vendor`` directory::

    $ cd your-project-name
    $ pip install -r requirements.txt -t vendor

**Note: App Engine can only import libraries from inside your project directory.**

You should now be able to run your project locally from the command line using
the regular Appengine SDK tools::

    $ dev_appserver.py .

Visit the application http://localhost:8080

See `the development server documentation`_ for options when running
dev\_appserver.py.


Deploying your application
--------------------------

To deploy your application you first need to ensure you've created a project
using the appengine `Admin Console`_. Once created, you can `deploy your
application`_ with the following command::

    $ appcfg.py -A <your-project-id> --oauth2 update .

Congratulations! Your application is now live at your-project-id.appspot.com


Installing additional libraries
-------------------------------

See the `Third party libraries`_ page for libraries that are already included
in the SDK. To include SDK libraries, add them in your app.yaml file. Other
than libraries included in the SDK, only pure python libraries may be added to
an App Engine project.

To install additional libraries from `pypi`_ you can use pip, e.g. to install
the `raven`_ library for reporting errors to a sentry server, simply run::

    $ pip install raven -t vendor


.. _App Engine Python SDK: https://developers.google.com/appengine/downloads
.. _pip: http://www.pip-installer.org/en/latest/installing.html
.. _the development server documentation: https://developers.google.com/appengine/docs/python/tools/devserver
.. _Admin Console: https://appengine.google.com
.. _deploy your application: https://developers.google.com/appengine/docs/python/tools/uploadinganapp
.. _Third party libraries: https://developers.google.com/appengine/docs/python/tools/libraries27
.. _pypi: https://pypi.python.org
.. _raven: https://pypi.python.org/pypi/raven
