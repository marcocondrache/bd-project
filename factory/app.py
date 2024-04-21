from importlib import import_module
from flask import Flask, render_template
from werkzeug.utils import import_string


class Base(Flask):
    def configure(self, config):
        self.config.from_object(config)

    def configure_modules(self):
        modules = self.config.get('BLUEPRINTS', [])

        for blueprint in modules:
            try:
                module = import_module('app.modules.%s' % blueprint)
                self.register_blueprint(getattr(module, blueprint))
            except Exception as e:
                print(e)
                self.logger.error('Error registering %s' % blueprint)

    def configure_error_handlers(self):
        @self.errorhandler(500)
        def internal_error(_):
            return render_template("http/500.html"), 500

        @self.errorhandler(404)
        def not_found(_):
            return render_template("http/404.html"), 404

    def configure_extensions(self):
        extensions = self.config.get('EXTENSIONS', [])

        for extension in extensions:
            ext = import_string(extension)
            init = getattr(ext, 'init_app', False) or ext

            # load additional kwargs
            try:
                init_kwargs = import_string('%s_init_kwargs' % extension)()
            except ImportError:
                init_kwargs = dict()
            init(self, **init_kwargs)

    def setup(self):
        self.configure_modules()
        self.configure_extensions()
        self.configure_error_handlers()
