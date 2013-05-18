"""
Simple base model to provide common
functions/properties for all our datastore entities.
"""
# third-party imports
from google.appengine.ext import ndb

# local imports
from cms.utils.list_widgets import DatetimeWidget
from cms.utils.list_widgets import DeleteWidget
from cms.utils.list_widgets import EditWidget


class BaseModel(ndb.Model):

    # record creation and modification times of entity
    creation_time = ndb.DateTimeProperty(auto_now_add=True)
    modification_time = ndb.DateTimeProperty(auto_now=True)

    def to_dict(self, *args, **kwargs):
        d = super(BaseModel, self).to_dict(*args, **kwargs)
        d['id'] = self.key.id()
        return d

    class Meta(object):
        """
        Model meta-config (CMS Form config etc.)
        """

        # icon to display in CMS header section for this model, see
        # http://fortawesome.github.io/Font-Awesome/ for available icons
        header_icon = 'icon-th-list'
        header_title = None
        # text to display in the blue permalert box in the CMS header
        header_help = None
        header_text = None
        custom_list_template = None
        default_sort_property = 'creation_time'
        default_sort_order = 'desc'

        # properties to display in table
        list_columns = [
            {'property': 'key', 'title': 'ID', 'sortable': True, 'display': lambda x: x.id()},
            {'property': 'creation_time', 'title': 'Created', 'sortable': True, 'display': DatetimeWidget()},
        ]

        list_actions = [EditWidget(), DeleteWidget()]
