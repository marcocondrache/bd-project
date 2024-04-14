from flask import Flask, render_template

class Base(Flask):
    def configure(self, config):
        self.config = config

    def configure_error_handlers(self):
        @self.errorhandler(500)
        def internal_error():
            return render_template("http/500.html"), 500
        
        @self.errorhandler(404)
        def not_found():
            return render_template("http/404.html"), 404
        
    def setup(self):
        pass
        