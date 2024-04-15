import os

from extentions import db
class Prod(object):
    ENV = os.getenv("FLASK_ENV", "production")
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'

    TESTING = False

    DB_USER = os.getenv('DB_USER', '')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_NAME = os.getenv('DB_NAME', '')

    SQLALCHEMY_DATABASE_URI = "" % {
        'user': DB_USER,
        'passwd': DB_PASS,
        'host': DB_HOST,
        'name': DB_NAME
    }

    BLUEPRINTS = ["auth"]
    EXTENSIONS = [db]

class Dev(Prod):
    DEBUG = True