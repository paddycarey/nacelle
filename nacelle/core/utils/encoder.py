# stdlib imports
import datetime
import json

# third-party imports
from google.appengine.api import datastore_types
from google.appengine.ext import ndb


class ModelEncoder(json.JSONEncoder):

    """
    Custom JSON encoder allowing easy encoding
    of appengine ndb entities/queries to JSON.
    """

    def default(self, obj):

        # convert models to dicts before serialising
        if isinstance(obj, ndb.Model):
            return obj.to_dict()

        # convert keys to ids
        if isinstance(obj, ndb.Key):
            return obj.get().key.id()

        # fetch the result of Ndb Futures
        if isinstance(obj, ndb.Future):
            return obj.get_result()

        # listify queries
        if isinstance(obj, ndb.Query):
            return list(obj.iter())

        # serialize geopts
        if isinstance(obj, datastore_types.GeoPt):
            return ','.join([str(obj.lat), str(obj.lon)])

        # output dates/times in iso8601 format
        if isinstance(obj, (datetime.date, datetime.datetime, datetime.time)):
            return obj.isoformat()

        # Let the base class default method raise the TypeError
        return super(ModelEncoder, self).default(obj)
