from flask import Blueprint

auth = Blueprint('sellers', __name__, template_folder="sellers", url_prefix="/sellers")

from app.modules.sellers import views
