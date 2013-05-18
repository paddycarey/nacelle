"""
Oauth related functions, validating tokens, making authorised API calls etc.
"""
# stdlib imports
import datetime
import jinja2
import json
import logging
import time
from xml.dom import minidom
from xml.parsers.expat import ExpatError

# third-party imports
from google.appengine.api import urlfetch

# local imports
from nacelle.api_clients import base


def post_image(image_data, access_token, url):

    # attempt the actual upload using the authorized_request function
    response = base.make_authorized_request(
        url,
        access_token,
        headers={
            'Content-Type': 'image/png',
            'GData-Version': '2',
        },
        method=urlfetch.POST,
        payload=image_data,
        deadline=60,
    )

    # parse and return the JSON response
    try:
        json_response = json.loads(response.content)
    except ValueError:
        logging.debug('Picasa response: %s' % response.content)
        raise
    return json_response


def post_image_to_picasa(image_data, credentials, album_id):

    """
    Post the given image to the picasa account of the user who owns
    the passed Auth token
    """

    # URL to use to post image to Picasa
    url = "https://picasaweb.google.com/data/feed/api/user/default/albumid/%s?alt=json"
    url = url % album_id

    return post_image(image_data, credentials, url)


new_album_template = jinja2.Template("""<entry xmlns='http://www.w3.org/2005/Atom' xmlns:media='http://search.yahoo.com/mrss/' xmlns:gphoto='http://schemas.google.com/photos/2007'>
<title type='text'>{{ name }}</title>
<summary type='text'>{{ summary }}</summary>
<gphoto:location>{{ location }}</gphoto:location>
<gphoto:access>public</gphoto:access>
<gphoto:timestamp>{{ "%d" % timestamp }}</gphoto:timestamp>
<media:group>
<media:keywords></media:keywords>
</media:group>
<category scheme='http://schemas.google.com/g/2005#kind' term='http://schemas.google.com/photos/2007#album'></category>
</entry>""")


def create_album(name, location, credentials):

    timestamp = time.mktime(datetime.datetime.utcnow().timetuple()) * 1000
    payload = new_album_template.render(name=name, location=location, timestamp=timestamp)

    response = base.make_authorized_request(
        "http://picasaweb.google.com/data/feed/api/user/default",
        credentials,
        auth_type='authsub',
        method=urlfetch.POST,
        follow_redirects=True,
        payload=payload,
        headers={
            'Content-Type': "application/atom+xml"
        }
    )
    # logging.info(response.content)
    try:
        album = minidom.parseString(response.content)
    except ExpatError:
        raise Exception("Could not create new album (%s)" % response.content)
    else:
        # return the newly created album's ID
        return album.getElementsByTagName("id")[0].firstChild.data.split("/")[-1]


def get_album(album_id, credentials):

    url = "https://picasaweb.google.com/data/feed/api/user/default/albumid/" + album_id + '?alt=json'
    response = base.make_authorized_request(url, credentials)
    rsjs = json.loads(response.content)['feed']
    return rsjs
