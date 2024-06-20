from uuid import UUID

from flask import request, render_template, url_for, redirect, abort, flash, current_app, g
from flask_login import login_required, current_user

from app.modules.carts.handlers import get_reservation_by_product
from app.modules.products import products
from app.modules.products.forms import SearchForm
from app.modules.products.handlers import (
    create_product, get_seller_products,
    get_all_product_categories, update_product, delete_product,
    get_product_by_guid, get_all_products
)
from app.modules.products.models import Product, ProductCategory, Keyword
from app.modules.shared.handlers import clean_expired_orders
from app.modules.shared.proxy import current_search
from app.modules.shared.utils import seller_required


def validate_product(product_guid: str, allow_write=False) -> Product | None:
    """
    Get a product by its guid.
    If the guid is not a valid UUID, throw a 400 error.
    If the product does not exist, throw a 404 error.
    For the edit and delete:
        If the user is not the owner of the product, throw a 403 error.
        If the product is locked, return None.
    :param product_guid: the guid of the product
    :param allow_write: check also for users write permissions
    :return: the product or None only if the product is locked
    """

    try:
        product_guid = UUID(product_guid)
        product = get_product_by_guid(product_guid)
        if not product:
            abort(404)
        if allow_write:
            if not current_user.sellers or product.owner_seller_id != current_user.sellers[0].id:
                abort(403)
            if product.locked_stock > 0:
                return None
        return product
    except ValueError:
        abort(400)


@products.route('', methods=['GET'])
@login_required
@seller_required
def index_view():
    page = request.args.get('page', 1, type=int)

    seller_products_pagination = get_seller_products(
        current_user.sellers[0].id, current_user.sellers[0].show_soldout_products, page=page
    )
    return render_template(
        'products/index.html',
        paginated_products=seller_products_pagination
    )


@products.route('/<product_guid>', methods=['GET'])
@login_required
def product_view(product_guid: str):
    product = validate_product(product_guid)
    if not product:
        return redirect(url_for('products.index_view'))

    product_reservation, sequence_failed = get_reservation_by_product(current_user.buyers[0].id, product)
    return render_template(
        'products/[guid].html',
        product=product,
        product_categories=[c.name for c in product.categories],
        categories=[c.name for c in get_all_product_categories()],
        product_reservation=product_reservation,
        sequence_failed=sequence_failed,
        is_seller_product=current_user.sellers and product.owner_seller_id == current_user.sellers[0].id
    )


@products.route('/<product_guid>/delete', methods=['POST'])
@login_required
@seller_required
def product_delete_view(product_guid: str):
    clean_expired_orders()

    product = validate_product(product_guid, allow_write=True)
    if not product:
        flash('An order is open for this product, all operations are temporarily disabled')
        return redirect(request.referrer or url_for('products.index_view'))

    delete_product(product)
    return redirect(url_for('products.index_view'))


@products.route('/<product_guid>/edit', methods=['POST', 'GET'])
@login_required
@seller_required
def product_edit_view(product_guid: str):
    clean_expired_orders()

    categories = get_all_product_categories()
    product = validate_product(product_guid, allow_write=True)

    if not product:
        flash('An order is open for this product, all operations are temporarily disabled')
        return redirect(url_for('products.product_view', product_guid=product_guid))

    if request.method == 'POST':
        new_price = float(request.form.get('price'))
        new_stock = int(request.form.get('stock'))
        new_categories = request.form.getlist('categories')
        new_description = request.form.get('description')

        if new_price < 0 or new_stock < 0:
            flash('Price and stock must be positive numbers')
            return render_template(
                'products/edit.html',
                product=product,
                categories=[c.name for c in categories],
                product_categories=[c.name for c in product.categories],
                section='your_products'
            )

        update_product(product, new_price, new_stock, new_categories, new_description)
        return redirect(url_for('products.product_view', product_guid=product_guid))

    return render_template(
        'products/edit.html',
        product=product,
        categories=[c.name for c in categories],
        product_categories=[c.name for c in product.categories]
    )


@products.route('/create', methods=['GET', 'POST'])
@login_required
@seller_required
def create_view():
    categories = get_all_product_categories()
    if request.method == 'POST':
        seller_id = current_user.sellers[0].id
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        if price < 0 or stock < 0:
            flash('Price and stock must be positive numbers')
            return render_template(
                'products/create.html',
                categories=[c.name for c in categories],
                section='your_products'
            )

        categories = request.form.getlist('categories')
        description = request.form.get('description')
        brand = request.form.get('brand')
        is_second_hand = request.form.get('is_second_hand') == 'on'

        create_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        return redirect(url_for('products.index_view'))

    return render_template(
        'products/create.html',
        categories=[c.name for c in categories]
    )


@products.route('/shop', methods=['GET'])
@login_required
def shop_products():
    def render(page):
        return render_template(
            'products/shop.html',
            page=page,
        )

    current_app.logger.info(current_search.data)

    seller_id = None
    if current_user.sellers:
        seller_id = current_user.sellers[0].id

    filters = [Product.owner_seller_id != seller_id, Product.deleted_at.is_(None)]

    page_num = current_search.page.data
    if current_search.validate():
        current_app.logger.info('correct validation')

        query_key = current_search.search.data
        category = current_search.category.data
        brands = current_search.brands.data
        price_min = current_search.price_min.data
        price_max = current_search.price_max.data

        query = Product.query

        if query_key:
            query = query.join(Product.keywords).filter(Keyword.key.ilike(query_key))

        if category and category != 'all':
            query = query.join(Product.categories).filter(ProductCategory.guid == category)

        if brands is not None and brands != []:
            query = query.filter(Product.brand.in_(brands))

        if price_min is not None and price_max is not None:
            query = query.filter(Product.price.between(price_min, price_max))

        return render(query.filter(*filters).paginate(page=page_num))
    else:
        current_app.logger.warn(current_search.errors)

    return render(get_all_products(filters=filters, page=page_num))
