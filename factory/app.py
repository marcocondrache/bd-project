from importlib import import_module

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from werkzeug.utils import import_string


class Base(Flask):
    def configure(self, config):
        self.config.from_object(config)

    def configure_modules(self):
        modules = self.config.get('BLUEPRINTS', [])

        for blueprint in modules:
            try:
                module = import_module(f'app.modules.{blueprint}')
                self.register_blueprint(getattr(module, blueprint))
            except Exception as e:
                self.logger.error(f'Error registering {blueprint}: {e}')

    def configure_error_handlers(self):
        @self.errorhandler(500)
        def internal_error(e):
            self.logger.error(e.description)
            return render_template("http/500.html", reason=e.description), 500

        @self.errorhandler(404)
        def not_found(e):
            self.logger.error(e.description)
            return render_template("http/404.html", reason=e.description), 404

        @self.errorhandler(403)
        def forbidden(e):
            self.logger.error(e.description)
            return render_template("index.html"), 403

        @self.errorhandler(CSRFError)
        def handle_csrf_error(e):
            self.logger.error(e.description)
            return '', 403

    def configure_extensions(self):
        extensions = self.config.get('EXTENSIONS', [])

        for extension in extensions:
            ext = import_string(extension)
            init = getattr(ext, 'init_app', False) or ext

            # load additional kwargs
            try:
                init_kwargs = import_string(f'{extension}_init_kwargs')()
            except ImportError:
                init_kwargs = dict()
            init(self, **init_kwargs)

    def setup(self):
        self.configure_modules()
        self.configure_extensions()
        self.configure_error_handlers()

        # TODO: find a better place for this
        self.jinja_env.trim_blocks = True
        self.jinja_env.lstrip_blocks = True
