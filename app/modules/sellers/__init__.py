from flask import Blueprint

sellers = Blueprint('sellers', __name__, url_prefix="/sellers")

from app.modules.sellers import views
