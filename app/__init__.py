import os
from importlib import import_module

from flask import request

from app.modules.products.forms import SearchForm
from app.modules.products.handlers import get_all_product_categories, get_all_product_brands
from factory.app import Base

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


def register_processor(app):
    @app.context_processor
    def injectors():
        categories = get_all_product_categories()
        brands = get_all_product_brands()

        search = SearchForm(data=request.args) if request.args else SearchForm()
        search.category.choices.extend([(c.guid, c.name) for c in categories])
        search.brands.choices.extend([(b[0], b[0]) for b in brands])
        return dict(search=search)


def read_config(path):
    if isinstance(path, str):
        module = import_module('config')
        return getattr(module, path)
    return path


def build(name, config_path, base_path=PROJECT_PATH):
    app = Base(name, root_path=base_path)
    config = read_config(config_path)

    app.configure(config)
    app.setup()

    register_processor(app)

    return app
