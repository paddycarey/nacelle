# local imports
from cms.handlers.base import CMSTemplateHandler


class IndexHandler(CMSTemplateHandler):

    def get(self):

        # render template and return
        return self.render_response('cms/index.html', {})
