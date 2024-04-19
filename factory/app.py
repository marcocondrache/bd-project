from importlib import import_module
from flask import Flask, render_template


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
        print(extensions)

        for extension in extensions:
            init = getattr(extension, 'init_app', False)
            init(self)
        
        migrate = self.config.get('MIGRATE', False)
        if migrate:
            migrate.init_app(self, extensions[0])

    def setup(self):
        self.configure_modules()
        self.configure_extensions()
        self.configure_error_handlers()
