# third-party imports
import webapp2
from oauth2client.client import OAuth2WebServerFlow

# local imports
import settings


def get_flow(request):

    """
    Returns a flow object to initiate the OAuth2 dance.
    """

    return OAuth2WebServerFlow(
        client_id=settings.OAUTH_CLIENT_ID,
        client_secret=settings.OAUTH_CLIENT_SECRET,
        scope=[
            'http://picasaweb.google.com/data/',
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/plus.pages.manage',
            'https://www.googleapis.com/auth/plus.me',
        ],
        redirect_uri=request.host_url + webapp2.uri_for('oauth-callback'),
        approval_prompt='force'
    )
