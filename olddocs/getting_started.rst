Getting Started With Nacelle
============================

Nacelle tries to be ready-to-run straight out of the box. The following guide attempts to quickly get you up and running with a basic nacelle app, for more advanced usage you should check out the full documentation (when it's completed).


Prerequisites
-------------

Nacelle has very few dependencies because it relies on included App Engine libraries and bundles everything else. Just make sure you have the latest Google App Engine SDK for Python installed.

If you want take advantage of unit testing, you'll need to install the following python packages:

 * `coverage <http://nedbatchelder.com/code/coverage/>`_ (required for code coverage metrics)
 * `coveralls <https://github.com/z4r/python-coveralls>`_ (nice online reporting of code coverage)
 * `nose <https://nose.readthedocs.org/en/latest/>`_ (extends unittest to make testing easier)
 * `yanc <https://github.com/0compute/yanc>`_ (color output plugin for nose that plays nicely with others)
 * `Pillow <http://python-imaging.github.io/>`_ (required for image service stub)


These packages can be easily installed with `pip <http://www.pip-installer.org/en/latest/>`_::

    pip install -r requirements.txt


Getting a copy of Nacelle
-------------------------

The latest version of Nacelle can be always be obtained from `Github <https://github.com/rehabstudio/nacelle>`_. You can either use git to clone Nacelle or download a copy of the master branch. Either way you do it, place the contents of the Nacelle's source into the directory where you will be creating your application.


App.yaml Configuration
----------------------

A little bit of configuration has to be done. Open up ``./app.yaml`` and set the application and version properties appropriately, like below::

    application: my-nacelle-app    #.appspot.com
    version: 1

You'll want to pick a unique application name in case you want to actually deploy this. For more information, check out the App Engine documentation.


Running with the App Engine development server
----------------------------------------------

Using the development server with a Nacelle application is the same as using it with any other App Engine applications. Just issue ``dev_appserver.py .`` on \*nix/Mac or use the `launcher <https://developers.google.com/appengine/training/intro/gettingstarted#starting>`_ on Windows. Once it's started you should be able to open up your app via http://localhost:8080. You should see a rather generic landing page.

.. note::
    If you're using the launcher, your URL may be slightly different. Make note of this as the tutorial and examples all use http://localhost:8080.
