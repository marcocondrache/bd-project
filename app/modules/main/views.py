from flask import render_template, redirect, url_for
from extensions import login_manager
from app.modules.main import main
from flask_login import current_user
from flask_login import login_required


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))


@main.route('/')
@login_required
def index():
    return redirect(url_for('home.index'))
