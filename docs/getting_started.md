# Getting Started with Nacelle

Nacelle tries to be ready-to-run straight out of the box. The following guide attempts to quickly get you up and running with a basic nacelle app, for more advanced usage you should check out the full documentation (when it's completed).


## Prerequisites

Nacelle has very few dependencies because it relies on included App Engine libraries and bundles everything else. Just make sure you have the latest Google App Engine SDK for Python installed.

If you want take advantage of unit testing, you'll need to install the development dependencies with pip:

    make install-devenv


## Getting a copy of Nacelle

The latest version of Nacelle can be always be obtained from [Github](https://github.com/rehabstudio/nacelle). You can either use git to clone Nacelle or download a copy of the master branch. Either way you do it, place the contents of the example directory in Nacelle's source where you will be creating your application.

    git clone https://github.com/rehabstudio/nacelle
    mkdir mynewapp
    cp -Lr nacelle/example/. mynewapp/


## App.yaml Configuration

A little bit of configuration has to be done. Open up ``./app.yaml`` and set the application and version properties appropriately, like below:

    application: my-nacelle-app    #.appspot.com
    version: 1

You'll want to pick a unique application name in case you want to actually deploy this. For more information, check out the App Engine documentation.


## Running with the App Engine development server

Using the development server with a Nacelle application is the same as using it with any other App Engine applications. Just issue ``dev_appserver.py .`` on \*nix/Mac or use the [launcher](https://developers.google.com/appengine/training/intro/gettingstarted#starting) on Windows. Once it's started you should be able to open up your app via http://localhost:8080. You should see a rather generic landing page.

Nacelle also includes a handy alias to make running the development server as easy as possible:

    make run

**If you're using the launcher, your URL may be slightly different. Make note of this as the tutorial and examples all use http://localhost:8080.**
