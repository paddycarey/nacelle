# stdlib imports
import json

# local imports
from nacelle.api_clients import base


def fetch_plus_page_info(credentials, page_id):

    """
    Fetch full profile details for a given G+ page ID
    """

    url = "https://www.googleapis.com/plusPages/v2/people/%s" % page_id
    response = base.make_authorized_request(url, credentials)
    # Parse the response data as a JSON object
    plus_page = json.loads(response.content)
    # return tuple of response status and response data
    return plus_page


def fetch_plus_pages(credentials):

    """
    Retrieve details of manageable G+ pages for a given access_token
    """

    # Build url and make an authorised request
    url = "https://www.googleapis.com/plusPages/v2/people/me/people/pages"
    response = base.make_authorized_request(url, credentials)
    # Parse the response data as a JSON object
    plus_pages = json.loads(response.content)
    # return tuple of response status and response data
    return plus_pages
