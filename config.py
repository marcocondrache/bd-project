import os

from dotenv import load_dotenv

load_dotenv()


class Prod(object):
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'

    TESTING = False

    SECRET_KEY = os.getenv('SECRET_KEY', '')

    DB_USER = os.getenv('DB_USER', '')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_NAME = os.getenv('DB_NAME', '')

    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

    BLUEPRINTS = ["home", "auth"]
    EXTENSIONS = [
        'extensions.db',
        'extensions.login_manager',
        'extensions.migrate'
    ]


class Dev(Prod):
    DEBUG = True
