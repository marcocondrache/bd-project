from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.modules.auth import auth
from app.modules.auth.handlers import validate_user, get_user_by_email, register_user


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember") == "on"

        subject = validate_user(email, password)
        if not subject:
            flash("Invalid credentials")
            return redirect(url_for("home.index"))
        login_user(subject, remember=remember)
        return redirect(url_for("home.index"))

    return render_template("auth/login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        given_name = request.form.get('given_name')
        family_name = request.form.get('family_name')
        password = request.form.get('password')
        password_confirmation = request.form.get('password_confirmation')
        destination_address = request.form.get('destination_address')
        card_number = request.form.get('card_number')

        existing_user = get_user_by_email(email)
        if existing_user:
            flash("User already exists")
            return render_template("auth/signup.html")

        if password != password_confirmation:
            flash("Passwords do not match")
            return render_template("auth/signup.html")

        # create user
        user = register_user(email, given_name, family_name, password, destination_address, card_number)
        login_user(user)
        return redirect(url_for("home.index"))

    return render_template("auth/signup.html")


@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
