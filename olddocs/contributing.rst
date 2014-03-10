============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given. 

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/rehabstudio/nacelle/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* A failing test case if possible

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Fix anything you can, if you're not sure about something, just ask.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the Github issues for already planned or in-development features and help out on one of those if you're interested.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

Write Documentation
~~~~~~~~~~~~~~~~~~~

Nacelle could always use more documentation, whether as part of the official docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/rehabstudio/nacelle/issues.


Get Started!
------------

Ready to contribute? Here's how to set up `nacelle` for local development.

1. Fork the `nacelle` repo on GitHub.
2. Clone your fork locally::

    $ git clone git@github.com:your_name_here/nacelle.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv nacelle
    $ cd nacelle/
    $ pip install -r requirements.txt

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature
   
   Now you can make your changes locally.

5. When you're done making changes, check that your tests pass::

    $ ./testrunner.sh

6. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
2. If the pull request adds functionality, the docs should be updated. Make sure to add the feature to the list in README.rst.
3. The pull request should work for Python 2.7. Check https://travis-ci.org/rehabstudio/nacelle/pull_requests and make sure that the tests pass.
