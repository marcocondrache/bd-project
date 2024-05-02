from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    page = IntegerField('Page', validators=[validators.Optional()], default=1)
    search = StringField('Search', validators=[validators.Optional()], render_kw={"placeholder": "Search products..."})