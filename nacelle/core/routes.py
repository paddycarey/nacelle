# third-party imports
from webapp2_extras.routes import MultiRoute


class MultiPrefixRoute(MultiRoute):
    """Combines the functionality of 3 different types of webbap2 prefix route
    because nesting's ugly.
    """

    def __init__(self, handler_pfx='', name_pfx='', path_pfx='', routes=None):

        assert isinstance(routes, list)
        super(MultiPrefixRoute, self).__init__(routes)
        self.prefix = path_pfx
        # Prepend a prefix to a route attribute.
        for route in self.get_routes():
            route.name = name_pfx + route.name
            route.template = path_pfx + route.template
            route.handler = handler_pfx + route.handler
