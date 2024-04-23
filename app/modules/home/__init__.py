from flask import Blueprint

home = Blueprint('home', __name__)

from app.modules.home import views
