from flask import Blueprint

reviews = Blueprint('reviews', __name__, url_prefix="/reviews")

from app.modules.reviews import views
