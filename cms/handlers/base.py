# third-party imports
import webapp2
from google.appengine.api import users
from webapp2_extras import sessions

# local imports
from cms.models.user import User
from nacelle.handlers.base import TemplateHandler
from settings import CMS_CONFIG


class CMSTemplateHandler(TemplateHandler):

    # bool to allow restricting
    # a handler to admins only
    admin_only = False

    def get_user(self):

        # get or create a user object as appropriate
        # for the currently logged in user
        user = users.get_current_user()
        if users.is_current_user_admin():
            user = User.get_or_insert_for_user(user=user)
        elif user is not None:
            user = User.get_for_user(user=user)
        return user

    def default_context(self):

        # ugh! locally scoped imports make paddy sad, but they're necessary
        # sometimes to prevent circular imports
        from cms.routes import build
        # ensure to populate the default context
        context = super(CMSTemplateHandler, self).default_context()
        try:
            context['cms_branding'] = CMS_CONFIG['branding']
        except KeyError:
            context['cms_branding'] = 'Nacelle CMS'
        context['cms_nav'] = build.get_nav()
        context['user'] = self.get_user()
        return context

    def dispatch(self):

        # ensure we have a session we can use
        self.session_store = sessions.get_store(request=self.request)

        # show login screen if not logged in
        if not users.get_current_user():
            self.session['redirect_url'] = self.request.path_qs
            # we need to explicitly store the session here as it normally
            # only gets stored after a succesful dispatch
            self.session_store.save_sessions(self.response)
            return self.redirect(self.uri_for('cms-login'))

        user = self.get_user()
        if user is None:
            self.session.add_flash("Unauthorised: You do not have permission to access this CMS")
            self.session['redirect_url'] = self.request.path_qs
            # we need to explicitly store the session here as it normally
            # only gets stored after a succesful dispatch
            self.session_store.save_sessions(self.response)
            return self.redirect(users.create_logout_url(self.uri_for('cms-login')))

        # dispatch request as normal
        super(CMSTemplateHandler, self).dispatch()
