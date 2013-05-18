# third-party imports
from google.appengine.api import users

# local imports
from nacelle.handlers.base import TemplateHandler


class LoginHandler(TemplateHandler):

    def get(self):

        # get redirect url from session
        redirect_url = self.session.get('redirect_url', self.uri_for('cms-index'))

        # render template and return
        context = {'login_url': users.create_login_url(redirect_url)}
        return self.render_response('cms/login.html', context)
