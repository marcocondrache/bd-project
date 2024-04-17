from flask import render_template
from app.modules.main import main


@main.route('/')
def index():
    return render_template("index.html")
