from flask import has_request_context, g, request, current_app
from flask_login import current_user
from werkzeug.local import LocalProxy

from app.modules.products.forms import SearchForm


def _get_search():
    """
    Utility function to get the search form. If the user is authenticated and the search form is not in the context,
    :return: the search form
    """
    if has_request_context() and current_user.is_authenticated:
        if "_search" not in g:
            return SearchForm(request.args)
        return g._search
    return None


current_search = LocalProxy(lambda: _get_search())
