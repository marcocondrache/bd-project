from app import build
import os

app = build("kepler-shop", os.environ.get('FLASK_CONFIG_DEFAULT', 'Prod'))

if __name__ == '__main__':
    _debug = app.config.get('DEBUG', False)

    startargs = {
        'host': os.getenv('FLASK_HOST', '0.0.0.0'),
        'port': int(os.getenv('FLASK_PORT', 8000)),
        'debug': _debug,
        'use_reloader': not app.config.get('USE_RELOADER', _debug),
        **app.config.get('SERVER_OPTIONS', {})
    }

    app.run(**startargs)
