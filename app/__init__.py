import os
from importlib import import_module

from flask import request

from app.modules.products.forms import SearchForm
from app.modules.products.handlers import get_all_product_categories, get_all_product_brands
from app.modules.shared.forms import PaginationForm
from app.modules.shared.proxy import current_search
from factory.app import Base

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))


def register_processors(app):
    @app.template_test("list")
    def is_list(obj):
        return isinstance(obj, list)

    @app.context_processor
    def injectors():
        pagination = PaginationForm(data=request.args)
        return dict(search=current_search, pagination=pagination)


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

    register_processors(app)

    return app
