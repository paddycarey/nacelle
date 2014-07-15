"""
Base test case that'll set up all the required appengine stubs for testing
"""
# stdlib imports
import sys
from unittest import TestCase

# third-party imports
from google.appengine.ext import testbed
from nacelle.conf import settings


class NacelleTestCase(TestCase):
    """
    Setup and teardown common to tests run using the appengine SDK
    """

    def __call__(self, result=None):
        """
        Wrapper around default __call__ method to perform common Nacelle test
        set up. This means that user-defined Test Cases aren't required to
        include a call to super().setUp().
        """
        testMethod = getattr(self, self._testMethodName)
        skipped = (getattr(self.__class__, "__unittest_skip__", False) or
                   getattr(testMethod, "__unittest_skip__", False))

        # pre-setup for any test methods
        if not skipped:
            try:
                self._pre_setup()
            except (KeyboardInterrupt, SystemExit):  # pragma: no cover
                raise
            except Exception:  # pragma: no cover
                result.addError(self, sys.exc_info())
                return

        # run the actual test methods being called
        super(NacelleTestCase, self).__call__(result)

        # post-teardown performed after that defined in the subclass
        if not skipped:
            try:
                self._post_teardown()
            except (KeyboardInterrupt, SystemExit):  # pragma: no cover
                raise
            except Exception:  # pragma: no cover
                result.addError(self, sys.exc_info())
                return

    def _pre_setup(self):
        # init testbed so we can use stubs to simulate the sandboxed environment
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.setup_env(overwrite=True, APPLICATION_ID='_')

        # INIT ALL THE STUBS!
        self.testbed.init_app_identity_stub()
        self.testbed.init_blobstore_stub()
        self.testbed.init_capability_stub()
        self.testbed.init_channel_stub()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_files_stub()
        # uncomment the below line to enable testing against the images API
        # self.testbed.init_images_stub()
        self.testbed.init_logservice_stub()
        self.testbed.init_mail_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub(root_path=settings.ROOT_DIR)
        self.testbed.init_urlfetch_stub()
        self.testbed.init_user_stub()
        self.testbed.init_xmpp_stub()

        self.taskq_stub = self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME)
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def _post_teardown(self):
        # clean up the testbed after each test is run
        self.testbed.deactivate()
