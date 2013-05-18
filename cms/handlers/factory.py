# local imports
from cms.handlers.skeleton import CMSBulkActionHandler
from cms.handlers.skeleton import CMSDeleteHandler
from cms.handlers.skeleton import CMSFormHandler
from cms.handlers.skeleton import CMSListTableHandler
from cms.handlers.skeleton import CMSListRowHandler


def list_handler(_model):

    """
    Returns a configured list view handler for the given ndb model
    """

    class ListTableHandler(CMSListTableHandler):
        model = _model

    return ListTableHandler


def row_handler(_model):

    """
    Returns a configured row view handler for the given ndb model
    """

    class ListRowHandler(CMSListRowHandler):
        model = _model

    return ListRowHandler


def form_handler(_model):

    """
    Returns a configured form handler for the given ndb model
    """

    class FormHandler(CMSFormHandler):
        model = _model

    return FormHandler


def delete_handler(_model):

    """
    Returns a configured delete entity handler for the given ndb model
    """

    class DeleteHandler(CMSDeleteHandler):
        model = _model

    return DeleteHandler


def bulk_action_handler(_model):

    """
    Returns a configured bulk action handler for the given ndb model
    """

    class BulkActionHandler(CMSBulkActionHandler):
        model = _model

    return BulkActionHandler
