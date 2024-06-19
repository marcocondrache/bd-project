from flask import Blueprint

shipments = Blueprint('shipments', __name__, url_prefix='/shipments')

from app.modules.shipments import views
