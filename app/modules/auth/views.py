from flask import render_template, request, session, redirect, url_for

from app.modules.auth import auth
from app.modules.auth.handlers import login_user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        subject = login_user(email, password)
        if subject:
            session["subject"] = subject
            return redirect(url_for("home.index"))
        return render_template("auth/login.html", error="Invalid credentials")

    # get request
    return render_template("auth/login.html")

@auth.route("/signup")
def signup():
    return render_template("auth/signup.html")
