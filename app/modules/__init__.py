from flask import Blueprint, render_template

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.errorhandler(404)
def not_found():
    return render_template("404.html"), 404

@main.errorhandler(500)
def internal_error():
    return render_template("500.html"), 500