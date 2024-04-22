from flask import Blueprint

products = Blueprint('products', __name__, url_prefix="/products")

from app.modules.products import views
