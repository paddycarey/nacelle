# third party imports
from markupsafe import Markup

# local imports
from nacelle.utils.stringutils import prettify_string


##################
# Column Widgets #
##################

class BooleanWidget(object):

    def __call__(self, prop):
        if prop:
            return Markup(u'<i class="icon-ok-sign"></i>')
        else:
            return Markup(u'<i class="icon-remove-sign"></i>')


class DatetimeWidget(object):

    def __init__(self, format=None):
        self.format = format or '%Y-%m-%d %H:%M:%S'

    def __call__(self, prop):
        return Markup(u'%s') % prop.strftime(self.format)


class ImageWidget(object):

    def __init__(self, max_height=36, max_width=36):
        self.max_height = int(max_height)
        self.max_width = int(max_width)

    def __call__(self, prop):
        return Markup(u'<img class="img-rounded" style="max-width: %dpx; max-height: %dpx;" src="%s">') % (self.max_width, self.max_height, prop)


class TextWidget(object):

    def __init__(self, truncate=False):
        self.truncate = int(truncate)

    def __call__(self, prop):
        if self.truncate:
            return Markup(u'%s') % prop[0:self.truncate].strip() + u'...'
        return Markup(u'%s') % prop


##################
# Action Widgets #
##################

class BaseActionWidget(object):

    """docstring for BaseActionWidget"""

    action = None
    level = 'info'
    icon = 'asterisk'

    @property
    def template(self):
        return u"""
            <a class="btn btn-%s btn-small" href="%s/%s/" title="%s {{ record.__class__.__name__ }}">
                <i class="icon-%s"></i> %s
            </a>
        """

    def __call__(self, record):

        pretty_action_name = prettify_string(self.action)
        template = Markup(self.template) % (self.level, self.action, str(record.key.id()), pretty_action_name, self.icon, pretty_action_name)
        return template


class DeleteWidget(BaseActionWidget):

    action = 'delete'
    level = 'danger'
    icon = 'remove'


class EditWidget(BaseActionWidget):

    action = 'edit'
    level = 'success'
    icon = 'edit'
