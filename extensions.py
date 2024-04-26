from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

login_manager = LoginManager()
login_manager.login_view = "auth.login"

migrate = Migrate()
csrf = CSRFProtect()

def migrate_init_kwargs():
    return {"db": db}
