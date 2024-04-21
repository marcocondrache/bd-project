from flask import Blueprint

home = Blueprint('home', __name__, template_folder="home", url_prefix="/home")

from app.modules.home import views
