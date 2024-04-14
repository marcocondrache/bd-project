from importlib import import_module
from flask import Flask, render_template

class Base(Flask):
    def configure(self, config):
        self.config.from_object(config)

    def configure_modules(self):
        modules = self.config.get('BLUEPRINTS', [])

        for module in modules:
            try:
                import_module('app.modules.%s' % module)
                self.register_blueprint(module)
            except Exception as e:
                print(e)
                self.logger.error('Error registering module %s' % module)

    def configure_error_handlers(self):
        @self.errorhandler(500)
        def internal_error(e):
            return render_template("http/500.html"), 500
        
        @self.errorhandler(404)
        def not_found(e):
            return render_template("http/404.html"), 404
        
    def configure_extensions(self):
        extensions = self.config.get('EXTENTIONS', [])

        for extention in extensions:
            init = getattr(extention, 'init_app', False)
            init(self)
        
    def setup(self):
        self.configure_modules()
        self.configure_extensions()
        self.configure_error_handlers()
        