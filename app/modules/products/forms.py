from flask_wtf import FlaskForm
from wtforms import validators, widgets
from wtforms.fields.choices import SelectField, SelectMultipleField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import SearchField

from app.modules.products.handlers import get_all_product_categories, get_all_product_brands, get_price_max, \
    get_stock_max


class SearchForm(FlaskForm):
    """
    Represents the search form. Used in the top bar.
    """
    class Meta:
        csrf = False

    page = IntegerField('Page', validators=[validators.Optional()], default=1)
    search = SearchField('Search', validators=[validators.Optional()],
                         render_kw={"placeholder": "Search products..."})

    category = SelectField(u'Category', validators=[validators.Optional()], choices=[('all', "All categories")])
    brands = SelectMultipleField(u'Brands', validators=[validators.Optional()], choices=[])

    price_max = IntegerField(u'To', validators=[validators.Optional()], widget=widgets.NumberInput())
    price_min = IntegerField(u'From', validators=[validators.Optional()], widget=widgets.NumberInput(min=0))

    stock_max = IntegerField(u'To', validators=[validators.Optional()], widget=widgets.NumberInput())
    stock_min = IntegerField(u'From', validators=[validators.Optional()], widget=widgets.NumberInput(min=0))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        categories = get_all_product_categories()
        brands = get_all_product_brands()
        price_max = get_price_max()
        stock_max = get_stock_max()

        self.category.choices.extend([(c.guid, c.name) for c in categories])
        self.brands.choices.extend([(b[0], b[0]) for b in brands])

        self.price_max.widget.max = price_max
        self.stock_max.widget.max = stock_max

    def filters_name(self):
        return [
            self.category.name,
            self.brands.name,
            self.price_max.name,
            self.price_min.name,
            self.stock_max.name,
            self.stock_min.name,
        ]
