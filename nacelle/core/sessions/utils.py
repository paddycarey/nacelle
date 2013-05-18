"""
Session related utilities
"""


def session(self):

    """
    Simple function that will be bound to the current request object to make
    the session retrievable inside a handler
    """

    # Returns a session using the default cookie key.
    return self.session_store.get_session()
