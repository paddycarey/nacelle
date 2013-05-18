# stdlib imports
import json
import logging

# third-party imports
import jinja2
from delorean import parse

# local imports
from nacelle.api_clients.base import make_oauthed_request
from nacelle.api_clients.base import make_request


class YoutubeError(Exception):
    pass


def fetch_feed(user_id):

    """
    Fetch videos uploaded by the given user and
    return as a list of dicts (cleaned up a bit)
    """

    # construct URL to get videos from
    feed_url = 'http://gdata.youtube.com/feeds/api/users/%s/uploads?alt=json&v=2&max-results=50' % user_id
    # use urlfetch service to make API call
    response = make_request(feed_url)
    if response.status_code in [403, 404]:
        return []
    # parse response as JSON
    try:
        response_json = json.loads(response.content)
    except ValueError:
        return []
    # process videos in feed
    try:
        feed = [process_video(x) for x in response_json['feed']['entry'] if is_embedable(x)]
    except KeyError:
        feed = []
    # return list of videos from API
    return feed


def fetch_playlists(ytuser=None):

    """
    Fetch all public playlists from the authorised user's account
    """
    # default url to call
    url = 'http://gdata.youtube.com/feeds/api/users/%s/playlists?v=2&alt=json'
    # use default user of a different youtube user id
    if ytuser is None:
        url = url % 'default'
    else:
        url = url % ytuser
    response = make_oauthed_request(url)
    # parse response as JSON
    try:
        response_json = json.loads(response.content)
    except ValueError:
        return []
    # process playlists response and return
    try:
        playlists = [process_playlist(x) for x in response_json['feed']['entry']]
    except KeyError:
        playlists = []
    return playlists


def fetch_playlist(playlist_id):

    """
    Fetch videos from a given playlist and
    return as a list of dicts (cleaned up a bit)
    """

    # construct URL to get videos from
    playlist_url = 'http://gdata.youtube.com/feeds/api/playlists/%s?alt=json&v=2&max-results=50' % playlist_id
    # use urlfetch service to make API call
    response = make_request(playlist_url)
    # parse response as JSON
    response_json = json.loads(response.content)
    # process videos in feed
    feed = process_playlist(response_json['feed'])
    # return list of videos from API
    return feed


def create_playlist(title, description):

    """
    Create a youtube playlist with the given details
    """

    # url to create playlists
    playlist_url = 'http://gdata.youtube.com/feeds/api/users/default/playlists?alt=json&v=2'

    # jinja2 template string to build POST payload
    template = jinja2.Template('<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><title type="text">{{ title }}</title><summary>{{ description }}</summary></entry>')

    # render template using the passed info
    template = template.render(title=title, description=description)
    # make API to actually create playlist
    response = make_oauthed_request(playlist_url, payload=template, method='POST', headers={'Content-Type': 'application/atom+xml'})

    # parse response as JSON and process
    response_json = json.loads(response.content)
    playlist = process_playlist(response_json['entry'])
    return playlist


def delete_playlist(playlist_id):

    url = 'http://gdata.youtube.com/feeds/api/users/default/playlists/%s?alt=json&v=2'
    url = url % playlist_id
    response = make_oauthed_request(url, method='DELETE')

    # raise a youtube error if request was unsuccessful
    if not response.status_code == 200:
        print response.content
        message = 'Unable to delete playlist: %s' % playlist_id
        raise YoutubeError(message)
    # fetch the playlist and return it
    return fetch_playlists()


def add_video_to_playlist(playlist_id, video_id):

    # url to create playlists
    playlist_url = 'http://gdata.youtube.com/feeds/api/playlists/%s?alt=json&v=2' % playlist_id

    # jinja2 template string to build POST payload
    template = jinja2.Template('<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><id>{{ video_id }}</id></entry>')

    # render template using the passed info
    template = template.render(video_id=video_id)
    # make API to actually create playlist
    response = make_oauthed_request(playlist_url, payload=template, method='POST', headers={'Content-Type': 'application/atom+xml'})

    # raise a youtube error if request was unsuccessful
    if not response.status_code == 201:
        raise YoutubeError('Unable to add video to list: %s' % video_id)
    # fetch the playlist and return it
    return fetch_playlist(playlist_id)


def delete_video_from_playlist(playlist_id, video_id):

    url = 'http://gdata.youtube.com/feeds/api/playlists/%s/%s?alt=json&v=2'
    url = url % (playlist_id, video_id)
    response = make_oauthed_request(url, method='DELETE')

    # raise a youtube error if request was unsuccessful
    if not response.status_code == 200:
        print response.content
        message = 'Unable to delete video from list: %s' % video_id
        raise YoutubeError(message)
    # fetch the playlist and return it
    return fetch_playlist(playlist_id)


def move_video_in_playlist(playlist_id, video_id, new_position):

    # url to create playlists
    playlist_url = 'http://gdata.youtube.com/feeds/api/playlists/%s/%s?alt=json&v=2' % (playlist_id, video_id)

    # jinja2 template string to build POST payload
    template = jinja2.Template('<?xml version="1.0" encoding="UTF-8"?><entry xmlns="http://www.w3.org/2005/Atom" xmlns:yt="http://gdata.youtube.com/schemas/2007"><yt:position>{{ new_position }}</yt:position></entry>')

    # render template using the passed info
    template = template.render(new_position=int(new_position))
    # make API to actually create playlists
    response = make_oauthed_request(playlist_url, payload=template, method='PUT', headers={'Content-Type': 'application/atom+xml'})

    # raise a youtube error if request was unsuccessful
    if not response.status_code == 200:
        raise YoutubeError('Unable to move video in playlist: %s' % video_id)
    # fetch the playlist and return it
    return fetch_playlist(playlist_id)


def update_videos_in_playlist(playlist_id, video_ids):

    """
    This function accepts a list of youtube video ids and
    updates a playlist with those videos in that order
    """

    # remove all existing videos from playlist
    for video in fetch_playlist(playlist_id)['feed']:
        try:
            playlist = delete_video_from_playlist(playlist_id, video['playlist_entry_id'])
        except YoutubeError, e:
            # assume the video was deleted and move on as that's the
            # only reason this func will throw a YoutubeError
            logging.warning(e)

    # readd videos to playlist in correct order
    for video_id in video_ids:
        playlist = add_video_to_playlist(playlist_id, video_id)
    else:
        playlist = fetch_playlist(playlist_id)

    return playlist


def fetch_video(video_id):

    """
    Fetch video from youtube API and return as processed dict
    """

    # construct URL to get videos from
    video_url = 'http://gdata.youtube.com/feeds/api/videos/%s?alt=json&v=2' % video_id
    # use urlfetch service to make API call
    response = make_request(video_url)
    # check if the video url returns a 404 and return None if it does
    if response.status_code == 404:
        return None
    # check if video has been made private (youtube v2 API doesn't
    # respect the json url param when this happens and so we can't
    # parse the response that way)
    if response.status_code == 403 and 'Private video' in response.content:
        return None
    # parse response as JSON
    try:
        response_json = json.loads(response.content)
    except ValueError:
        logging.warning('Unable to parse Youtube API response')
        raise
    # process videos in feed
    video = process_video(response_json['entry'])
    # return list of videos from API
    return video


def process_playlist(entry):

    """
    Clean up a playlist response from the youtube API
    """

    # extract required fields
    playlist = {
        'id': entry['yt$playlistId']['$t'],
        'title': entry['title']['$t'],
        'copyright': entry['author'][0]['name']['$t'],
        'date': parse(entry['updated']['$t']).naive(),
    }
    # process video objects if available
    if 'entry' in entry:
        playlist['feed'] = [process_video(x, in_playlist=True) for x in entry['entry']]
    else:
        playlist['feed'] = []

    return playlist


def process_video(entry, in_playlist=False):

    """
    Map video data from the Youtube API into something
    that makes a little more sense for our purposes
    """

    # give some output so that the user knows we're doing something
    logging.debug('Fetching video details: %s' % entry['media$group']['yt$videoid']['$t'])

    # TODO: Add check for if video is embeddable
    # TODO: Add check to ensure video is not georestricted in UK

    video = {
        # video's youtube ID
        'code': entry['media$group']['yt$videoid']['$t'],
        # video's title
        'title': entry['title']['$t'],
        # longform description of video
        'description': entry['media$group']['media$description']['$t'],
        # datetime that the video was published on youtube
        'published': parse(entry['published']['$t']).naive(),
        # largest thumbnail image that is available via the API
        'image': sorted(entry['media$group']['media$thumbnail'], key=lambda k: k['width'])[-1]['url'],
        # video owner name
        'owner_name': entry['media$group']['media$credit'][0]['yt$display'],
        'owner_id': entry['media$group']['media$credit'][0]['$t'],
    }

    # we need to check manually for rating and statistic values
    # as they might not be present in all videos
    try:
        # number of favourites for this video
        video['favourites'] = int(entry['yt$statistics']['favoriteCount'])
    except KeyError:
        video['favourites'] = 0
    try:
        # number of views for this video
        video['views'] = int(entry['yt$statistics']['viewCount'])
    except KeyError:
        video['views'] = 0
    try:
        # number of likes for this video
        video['likes'] = int(entry['yt$rating']['numLikes'])
    except KeyError:
        video['likes'] = 0
    try:
        # number of dislikes for this video
        video['dislikes'] = int(entry['yt$rating']['numDislikes'])
    except KeyError:
        video['dislikes'] = 0

    # check if this video has georestrictions attatched
    video['georestrict_allowed'] = []
    video['georestrict_denied'] = []
    try:
        restrictions = entry['media$group']['media$restriction']
    except KeyError:
        pass
    else:
        for restriction in restrictions:
            if restriction['type'] == 'country' and restriction['relationship'] == 'allow':
                video['georestrict_allowed'] = restriction['$t'].split()
            elif restriction['type'] == 'country' and restriction['relationship'] == 'deny':
                video['georestrict_denied'] = restriction['$t'].split()

    # add the playlist entry id if in a playlist
    if in_playlist:
        video['playlist_entry_id'] = entry['id']['$t'].rsplit(':', 1)[1]

    return video


def validate_user(user_id):

    """
    Make a HEAD request to a youtube API endpoint to validate
    that a given user id actually exists (for validation purposes only)
    """

    # API endpoint URL
    profile_url = 'http://gdata.youtube.com/feeds/api/users/%s?alt=json&v=2' % user_id
    # make the HEAD request
    response = make_request(profile_url, method='HEAD')
    # return True on a succesful check
    if response.status_code == 200:
        return True
    # log the error and return false on a failed check
    logging.warning('Invalid youtube user: %s' % user_id)
    logging.warning(response.content)
    return False


def is_embedable(video_entry):

    formats = [x['yt$format'] for x in video_entry['media$group']['media$content']]
    return 5 in formats
