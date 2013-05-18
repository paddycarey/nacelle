# third-party imports
from google.appengine.ext import ndb

# local imports
from cms.utils.list_widgets import DatetimeWidget
from nacelle.models.base import BaseModel


class Category(BaseModel):

    """
    Model to allow storing of categories for blog posts.
    """

    class Meta(BaseModel.Meta):
        """
        Model meta-config (CMS Form config etc.)
        """

        # properties to display in table
        list_columns = [
            {'property': 'name', 'sortable': True},
            {'property': 'creation_time', 'title': 'Created', 'sortable': True, 'display': DatetimeWidget(format='%Y-%m-%d')},
        ]

    name = ndb.StringProperty(required=True)
