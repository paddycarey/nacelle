from sniffer.api import * # import the really small API
import os, termstyle

# you can customize the pass/fail colors like this
pass_fg_color = termstyle.green
pass_bg_color = termstyle.bg_default
fail_fg_color = termstyle.red
fail_bg_color = termstyle.bg_default

# this gets invoked on every file that gets changed in the directory. Return
# True to invoke any runnable functions, False otherwise.
#
# This fires runnables only if files ending with .py extension and not prefixed
# with a period.
@file_validator
def py_files(filename):
    return filename.endswith('.py') and not os.path.basename(filename).startswith('.')

# This gets invoked for verification. This is ideal for running tests of some sort.
# For anything you want to get constantly reloaded, do an import in the function.
#
# sys.argv[0] and any arguments passed via -x prefix will be sent to this function as
# it's arguments. The function should return logically True if the validation passed
# and logicially False if it fails.
#
# This example simply runs nose.
@runnable
def execute_nose(*args):
    # setup our appengine environment so we can import the libs we need for our tests,
    # we need to do this first so we can import the stubs from testbed
    from nacelle.test.environ import setup_environ
    setup_environ()
    import nose
    return nose.run(argv=['sniffer.py', '-v', '--with-cover', '--cover-package=app,nacelle', '--cover-inclusive', '--cover-erase', '--with-yanc', '--logging-level=INFO'])
