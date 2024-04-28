from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, HiddenField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    page = IntegerField('Page', validators=[validators.optional()], default=1)
    search = StringField('Search', validators=[validators.data_required()], render_kw={"placeholder": "Search products..."})