# local imports
from nacelle.handlers.base import TemplateHandler


class DefaultIndexHandler(TemplateHandler):

    def get(self):
        _template = 'default/welcometonacelle.html'
        return self.render_response(_template, {})
