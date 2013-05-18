# stdlib imports
import datetime
import json

# third-party imports
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

        # output dates/times in iso8601 format
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

        return super(ModelEncoder, self).default(obj)
