from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.numeric import IntegerField


class PaginationForm(FlaskForm):
    """
    Represents the pagination form.
    """
    page = IntegerField("Page", validators=[validators.Optional()], default=1)
