# stdlib imports
import hashlib
import urllib

# third-party imports
from google.appengine.ext import ndb
from wtforms import validators

# local imports
from cms.utils.list_widgets import DatetimeWidget
from cms.utils.list_widgets import ImageWidget
from nacelle.models.base import BaseModel


class User(BaseModel):

    """
    Model to allow storing of admin user details.
    """

    class Meta(BaseModel.Meta):
        """
        Model meta-config (CMS Form config etc.)
        """

        # icon to display in CMS header section for this model, see
        # http://fortawesome.github.io/Font-Awesome/ for available icons
        header_icon = 'icon-group'
        # text to display in the blue permalert box in the CMS header
        header_text = 'User accounts allow users to access this CMS. Users without a Google account will be prompted to sign up for one upon first login to the CMS.'

        # specify a custom constructor to use for creating
        # the entity when a new form is processed, specified
        # as a tuple of strings, first the method name then any
        # arguments to be passed from the form, as strings
        form_constructor = ('create_from_form', 'email')

        # properties to display in table
        list_columns = [
            {
                'property': 'gravatar',
                'title': '',
                'display': ImageWidget()
            },
            {
                'property': 'email',
                'sortable': True
            },
            {
                'property': 'name',
                'sortable': True
            },
            {
                'property': 'creation_time',
                'title': 'Created',
                'sortable': True,
                'display': DatetimeWidget(format='%Y-%m-%d %H:%M')
            },
        ]

    # email will either be set on creation of a new
    # user by a super admin or when a super admin
    # logs in for the first time
    email = ndb.StringProperty(required=True)
    name = ndb.StringProperty()

    @classmethod
    def build_key(cls, email):
        # md5 hash of the user's email to use as entity key
        return hashlib.md5(email).hexdigest()

    @classmethod
    def get_or_insert_for_user(cls, user):

        """
        Alternate constructor to transactionally retrieve or create a User entity
        for the given google.appengine.api.users.User object.
        """

        user_entity = cls.get_or_insert(cls.build_key(user.email()), email=user.email())
        return user_entity

    @classmethod
    def get_for_user(cls, user):

        """
        Alternate constructor to retrieve a User entity
        for the given google.appengine.api.users.User object.
        """

        user_entity = cls.get_by_id(cls.build_key(user.email()))
        return user_entity

    @classmethod
    def create_from_form(cls, email):
        user_key = cls.build_key(email)
        return cls(id=user_key, email=email)

    @property
    def gravatar(self):

        """
        Returns a gravatar URL for this user
        """

        # append md5 hashed email and desired image size to base url
        gravatar_url = "//www.gravatar.com/avatar/"
        gravatar_url += hashlib.md5(self.email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'s': str(200)})
        return gravatar_url
