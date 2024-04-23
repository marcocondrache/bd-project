from flask import Blueprint

users = Blueprint('users', __name__, url_prefix="/users")

from app.modules.users import views
