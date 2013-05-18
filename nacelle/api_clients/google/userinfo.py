# stdlib imports
import json

# local imports
from nacelle.api_clients.base import make_authorized_request


def get_userinfo(credentials):

    """
    Get user details from the google userinfo API
    """

    url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    response = make_authorized_request(url, credentials)
    return json.loads(response.content)
