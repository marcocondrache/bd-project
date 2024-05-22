from flask import Blueprint

carts = Blueprint('carts', __name__, url_prefix="/carts")

from app.modules.carts import views
