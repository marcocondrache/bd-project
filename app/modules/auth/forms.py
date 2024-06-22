from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.simple import StringField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    """
    Form for logging in.
    """
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email(message="Invalid email format")])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    remember = BooleanField('Remember me', validators=[validators.Optional()], default=False)
