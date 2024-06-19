from flask import has_request_context, g, request
from flask_login import current_user
from werkzeug.local import LocalProxy

from app.modules.products.forms import SearchForm
from app.modules.products.handlers import get_all_product_categories, get_all_product_brands, get_price_max


def _get_search():
    if has_request_context() and current_user.is_authenticated:
        if "_search" not in g:
            categories = get_all_product_categories()
            brands = get_all_product_brands()
            price_max = get_price_max()

            form = SearchForm(request.args)

            form.category.choices.extend([(c.guid, c.name) for c in categories])
            form.brands.choices.extend([(b[0], b[0]) for b in brands])
            form.price_max.widget.max = price_max

            return form
        return g._search
    return None


current_search = LocalProxy(lambda: _get_search())
