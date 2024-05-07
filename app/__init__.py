from importlib import import_module

from flask import request

from app.modules.products.forms import SearchForm
from app.modules.products.handlers import get_all_product_categories
from factory.app import Base


def register_processor(app):
    @app.context_processor
    def injectors():
        search = SearchForm(data=request.args) if request.args else SearchForm()
        categories = get_all_product_categories()
        return dict(search=search, categories=categories)


def read_config(path):
    if isinstance(path, str):
        module = import_module('config')
        return getattr(module, path)
    return path


def build(name, config_path, base_path="app"):
    app = Base(name, root_path=base_path)
    config = read_config(config_path)

    app.configure(config)
    app.setup()

    register_processor(app)

    return app
