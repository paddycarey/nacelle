# stdlib imports
import urllib

# third-party imports
import webapp2


def modify_query_string(request, **kwargs):

    """
    Simple method to create a query string changing only
    one parameter in the request
    """

    # we can't modify the request params in place so
    # we need to make a copy of the dict
    temp = request.GET.copy()

    # loop over kwargs, deleting params from the query
    # string if they've been specified with an empty string,
    # otherwise we update the query string with the specified
    # value and reencode before returning
    for key, value in kwargs.items():
        if value == '':
            try:
                del temp[key]
            except:
                pass
        else:
            temp[key] = value

    # return encoded query string
    return urllib.urlencode(temp)


def nav_match(path, routes):

    """
    Match the specified path against a list of
    route names, returning true if matched
    """

    assert isinstance(routes, list)
    for route in routes:
        if path.startswith(webapp2.uri_for(route)):
            return True
    return False
