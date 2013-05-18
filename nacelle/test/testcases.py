"""
Base test case that'll set up all the required appengine stubs for testing
"""
# stdlib imports
import sys
from unittest import TestCase

# third-party imports
from google.appengine.ext import testbed


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
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                result.addError(self, sys.exc_info())
                return

        # run the actual test methods being called
        super(NacelleTestCase, self).__call__(result)

        # post-teardown performed after that defined in the subclass
        if not skipped:
            try:
                self._post_teardown()
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                result.addError(self, sys.exc_info())
                return

    def _pre_setup(self):
        # init testbed so we can use stubs to simulate the sandboxed
        # environment
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # INIT ALL THE STUBS!
        self.testbed.init_all_stubs()

    def _post_teardown(self):
        # clean up the testbed after each test is run
        self.testbed.deactivate()
