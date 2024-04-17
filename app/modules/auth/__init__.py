from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder="auth", url_prefix="/auth")

from app.modules.auth import views
