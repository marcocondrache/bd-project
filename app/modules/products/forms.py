from flask_wtf import FlaskForm
from wtforms import validators, widgets
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.numeric import IntegerField, IntegerRangeField
from wtforms.fields.simple import StringField, SearchField


class SearchForm(FlaskForm):
    class Meta:
        csrf = False

    page = IntegerField('Page', validators=[validators.Optional()], default=1)
    search = SearchField('Search', validators=[validators.Optional()],
                         render_kw={"placeholder": "Search products..."})

    category = SelectField(u'Category', validators=[validators.Optional()], choices=[('all', "All categories")])
    brands = SelectMultipleField(u'Brands', validators=[validators.Optional()], choices=[])

    price_max = IntegerField(u'Price Max', validators=[validators.Optional()])
    price_min = IntegerField(u'Price Min', validators=[validators.Optional()], widget=widgets.NumberInput(min=0))
