"""
Custom dispatcher for nacelle that implements session support
"""
# third-party imports
import webapp2
from webapp2_extras import sessions

# local imports
from nacelle.core.sessions.utils import session


def nacelle_dispatcher(router, request, response):

    """
    Override dispatch to provide session support
    """

    # Get a session store for this request.
    request.session_store = sessions.get_store(request=request)
    request.session = session.__get__(request, webapp2.Request)

    try:
        # Dispatch the request.
        response = router.default_dispatcher(request, response)
    finally:
        # Save all sessions.
        request.session_store.save_sessions(response)
    return response
