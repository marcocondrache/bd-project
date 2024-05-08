from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.list import FieldList
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, SearchField


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    page = IntegerField('Page', validators=[validators.Optional()], default=1)
    search = SearchField('Search', validators=[validators.DataRequired()],
                         render_kw={"placeholder": "Search products..."})

    category = FieldList(StringField('', validators=[validators.Optional()]), default=[])
