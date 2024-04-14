from factory.app import Base

basestring = getattr(__builtins__, 'basestring', str)

def read_config(path):
    if isinstance(path, basestring):
        module = __import__('config', fromlist=[path])
        return getattr(module, path)
    return path

def build(name, config_path):
    app = Base(name)
    config = read_config(config_path)

    app.configure(config)
    app.setup()

    return app

