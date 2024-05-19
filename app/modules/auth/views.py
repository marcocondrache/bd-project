from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user

from app.modules.auth import auth
from app.modules.auth.forms import LoginForm
from app.modules.auth.handlers import validate_user, get_user_by_email, register_user
from extensions import csrf


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            subject = validate_user(form.email.data, form.password.data)
            if not subject:
                flash("Invalid credentials")
                return redirect(url_for("auth.login"))

            login_user(subject, remember=form.remember.data)
        else:
            flash(next(iter(form.errors.values()))[0])

        return redirect(url_for("home.index_view"))

    return render_template("auth/login.html", form=form)


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
        return redirect(url_for("home.index_view"))

    return render_template("auth/signup.html")


@auth.route("/logout", methods=["GET"])
@csrf.exempt
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

