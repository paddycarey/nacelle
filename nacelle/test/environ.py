# stdlib imports
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

    # add the lib directory to the sytem path
    sys.path.insert(0, os.path.join(ROOT_PATH, 'vendor'))

    # Find the path on which the SDK is installed
    sdk_path = None
    for path in os.environ.get('PATH').split(os.pathsep):
        if not os.path.exists(path):
            continue
        if 'dev_appserver.py' in os.listdir(path):
            test_path = os.path.join(path, 'dev_appserver.py')
            sdk_path = os.path.dirname(os.readlink(test_path) if os.path.islink(test_path) else test_path)
            break

    # crap out if we can't find the SDK
    if not sdk_path:
        sys.stderr.write("Fatal: Can't find sdk_path")
        sys.exit(1)
    # add the SDK path to the system path
    sys.path.insert(0, sdk_path)

    # Use dev_appserver to set up the python path
    from dev_appserver import fix_sys_path
    fix_sys_path()

    from google.appengine.tools import dev_appserver as tools_dev_appserver
    from google.appengine import dist

    # Parse `app.yaml`
    appinfo, url_matcher, from_cache = tools_dev_appserver.LoadAppConfig(
        ROOT_PATH, {}, default_partition='dev')
    app_id = appinfo.application

    # Useful for later scripts
    os.environ['APPLICATION_ID'] = app_id
    os.environ['APPLICATION_VERSION'] = appinfo.version

    # Add third-party libs to the system path
    if appinfo.libraries:
        for library in appinfo.libraries:
            try:
                dist.use_library(library.name, library.version)
            except ValueError, e:
                if library.name == 'django' and library.version == '1.5':
                    # Work around an SDK issue
                    # print 'Warning: django 1.5 not recognised by dist, fixing python path'
                    sys.path.insert(0, os.path.join(sdk_path, 'lib', 'django-1.5'))
                elif library.name == 'jinja2' and library.version == '2.6':
                    sys.path.insert(0, os.path.join(sdk_path, 'lib', 'jinja2-2.6'))
                elif library.name == 'webapp2' and library.version == '2.5.2':
                    sys.path.insert(0, os.path.join(sdk_path, 'lib', 'webapp2-2.5.2'))
                elif library.name == 'webob' and library.version == '1.2.3':
                    sys.path.insert(0, os.path.join(sdk_path, 'lib', 'webob-1.2.3'))
                elif library.name == 'PIL':
                    try:
                        from PIL import Image
                    except ImportError:
                        print 'Warning: Make sure you have PIL installed locally'
                else:
                    print 'Warning: Unsupported library:\n%s\n' % e
