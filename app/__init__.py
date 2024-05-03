from importlib import import_module

from flask import request

from app.modules.products.forms import SearchForm
from factory.app import Base


def register_processor(app):
    @app.context_processor
    def injectors():
        search = SearchForm(data=request.args) if request.args else SearchForm()
        return dict(search=search)


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
