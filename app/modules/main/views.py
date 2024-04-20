from flask import render_template, redirect, url_for
from app.modules.main import main
from flask_login import current_user



@main.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('main/index.html')
    return redirect(url_for('auth.login'))
