from flask import redirect, url_for, render_template
from flask_login import login_required

from app.modules.home import home
from extensions import login_manager


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


@home.route('/')
@login_required
def index():
    return render_template('index.html', section='dashboard')
