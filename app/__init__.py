from importlib import import_module
from factory.app import Base


def read_config(path):
    if isinstance(path, str):
        module = import_module('config')
        return getattr(module, path)
    return path


def build(name, config_path, base_path="app"):
    app = Base(name, template_folder="templates", static_folder="static", root_path=base_path)
    config = read_config(config_path)

    app.configure(config)
    app.setup()

    return app
