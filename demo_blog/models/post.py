# third-party imports
from google.appengine.ext import ndb

# local imports
from cms.utils.list_widgets import BooleanWidget
from cms.utils.list_widgets import DatetimeWidget
from cms.utils.list_widgets import TextWidget
from cms.utils.list_widgets import BaseActionWidget
from cms.utils.list_widgets import DeleteWidget
from cms.utils.list_widgets import EditWidget
from demo_blog.models.category import Category
from nacelle.models.base import BaseModel


class PublishWidget(BaseActionWidget):

    action = 'publish'
    icon = 'eye-open'


class Post(BaseModel):

    """
    Model to allow storing of blog posts.
    """

    class Meta(BaseModel.Meta):
        """
        Model meta-config (CMS Form config etc.)
        """

        # icon to display in CMS header section for this model, see
        # http://fortawesome.github.io/Font-Awesome/ for available icons
        header_icon = 'icon-edit'
        header_title = 'Curate Blog Posts'
        # text to display in the blue permalert box in the CMS header
        header_text = 'Posts can be created or deleted from this view.'

        # properties to display on form
        form_fields = [
            {'property': 'title', 'args': {}},
            {'property': 'content', 'args': {}},
            {'property': 'published', 'args': {}},
            {'property': 'category', 'args': {'query': Category.query(), 'get_label': lambda x: x.name}},
        ]

        # properties to display in table
        list_columns = [
            {
                'property': 'title',
                'sortable': True
            },
            {
                'property': 'content',
                'display': TextWidget(truncate=200)
            },
            {
                'property': 'published',
                'sortable': True,
                'display': BooleanWidget()
            },
            {
                'property': 'category',
                'sortable': True,
                'display': lambda x: x.get().name,
            },
            {
                'property': 'creation_time',
                'title': 'Created',
                'sortable': True,
                'display': DatetimeWidget(format='%Y-%m-%d')
            },
        ]

        list_actions = [PublishWidget(), EditWidget(), DeleteWidget()]

    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(default='')
    published = ndb.BooleanProperty(default=False)
    category = ndb.KeyProperty(kind='Category')
