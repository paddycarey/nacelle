# stdlib imports
import distutils.spawn
import os
import sys

# get the app's path so we can use it in other places
THIS_DIR = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.normpath(os.path.join(THIS_DIR, os.pardir, os.pardir))


def setup_environ():

    """
    This func will import the required modules and set up enough of an
    appengine environment to let some of our management commands run inside the
    SDK sandbox
    """

    # add nacelle's vendor directory to the sytem path
    sys.path.insert(0, os.path.join(ROOT_PATH, 'nacelle', 'vendor'))

    # Find the path on which the SDK is installed
    test_path = distutils.spawn.find_executable('dev_appserver.py')
    if test_path is None:
        print "ERROR: Can't find sppengine SDK on your PATH"
        sys.exit(1)
    sdk_path = os.path.dirname(test_path)

    # add the SDK path to the system path
    sys.path.insert(0, sdk_path)

    # Use dev_appserver to set up the python path
    from dev_appserver import fix_sys_path
    fix_sys_path()
