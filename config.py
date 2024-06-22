import os

from dotenv import load_dotenv

load_dotenv()


class Prod(object):
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

    TESTING = False

    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24))

    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')

    if not DB_USER or not DB_PASS or not DB_HOST or not DB_NAME:
        raise ValueError("Missing database configuration: add DB_USER, DB_PASS, DB_HOST, DB_NAME to the .env file")

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_ENGINE_OPTIONS = {
        "isolation_level": "REPEATABLE READ",
    }

    BLUEPRINTS = ["home", "auth", "users", "buyers", "sellers", "products", "carts", "orders", "shipments"]
    EXTENSIONS = [
        'extensions.db',
        'extensions.login_manager',
        'extensions.migrate',
        'extensions.csrf',
        'extensions.cors'
    ]


class Dev(Prod):
    SQLALCHEMY_ENGINE_OPTIONS = {
        **super().SQLALCHEMY_ENGINE_OPTIONS,
        "echo": True,
    }
    
    DEBUG = True
