"""
Useful mixins to provide common functions
often used in various types of handler
"""
# third-party imports
import webapp2
from google.appengine.datastore.datastore_query import Cursor

# local imports
from nacelle.utils.pager import Pager


class QueryMixins(webapp2.RequestHandler):

    """
    Add this mixin class to any handler to enable simple query
    support, configurable and pageable via URL parameters
    """

    # model on which all requests to this handler will
    # run their queries (required)
    model = None

    # internal flag used to tell appengine to sort primarily by __key__ (needed
    # to enable appengine to efficiently dedupe when a query requires
    # intersection of the results of multiple independant queries)
    # N.B. You do need to set this manually in your subclass if you are using
    # intersecting queries
    _multiquery = False
    # default sort order for query if none specified
    default_sort = 'creation_time'

    def get_filters(self, query):

        """
        URL parameters for queries must be specified manually in each
        subclassed handler, to define a standard would, IMHO, severely limit
        the scope and usefulness of this mixin
        """

        return query

    def get_sorts(self, query):

        """
        Add sorting to our query
        """

        # get all sort orders from query string
        sort_orders = self.request.GET.getall('sort')

        if sort_orders:
            # loop over and add specified sort orders to query
            for sort_order in sort_orders:
                if sort_order.startswith('-'):
                    query = query.order(-getattr(self.model, sort_order[1:]))
                else:
                    query = query.order(getattr(self.model, sort_order))
        else:
            # order by creation time if no other order specified
            query = query.order(-getattr(self.model, self.default_sort))

        if self._multiquery:
            query = query.order(self.model.key)

        return query

    def get_query(self):

        """
        This is the main method which subclasses should call to retrieve
        query results and a cursor for the next page
        """

        # build query object
        q = self.model.query()

        # filter query as requested
        q = self.get_filters(q)

        # sort the query as requested
        q = self.get_sorts(q)

        # get page size from request
        page_number = self.request.get('page', 1)

        # fetch and paginate data
        return self.paginate(q, int(page_number))

    def paginate(self, query, page_number):

        """
        Paginate the result of a query
        """

        pager = Pager(query=query, page=page_number)
        page, _, _ = pager.paginate(page_size=50)
        return pager, page
