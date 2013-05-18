# stdlib imports
import errno
import os

# local imports
from nacelle.conf import settings


class TemplateNotFound(Exception):
    pass


def _open_if_exists(filename, mode='rb'):
    """Returns a file descriptor for the filename if that file exists,
    otherwise `None`.
    """
    try:
        return open(filename, mode)
    except IOError, e:
        if e.errno not in (errno.ENOENT, errno.EISDIR):
            raise


def _split_template_path(template):
    """Split a path into segments and perform a sanity check.  If it detects
    '..' in the path it will raise a `TemplateNotFound` error.
    """
    pieces = []
    for piece in template.split('/'):
        if os.path.sep in piece or (os.path.altsep and os.path.altsep in piece) or piece == os.path.pardir:
            raise TemplateNotFound(template)
        elif piece and piece != '.':
            pieces.append(piece)
    return pieces


def load_handlebars_template(template_path):
    pieces = _split_template_path(template_path)
    filename = os.path.join(settings.ROOT_DIR, 'templates', *pieces)
    f = _open_if_exists(filename)
    if f is None:
        raise TemplateNotFound(template_path)
    try:
        contents = f.read().decode('utf-8')
    finally:
        f.close()
    return contents.replace('\n', '')
