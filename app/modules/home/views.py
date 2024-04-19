from flask import render_template
from flask_login import login_required

from app.modules.home import home


@home.route('/')
@login_required
def index():
    return render_template('home/index.html')
