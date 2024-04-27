from uuid import UUID

from flask import request, render_template, url_for, redirect, abort
from flask_login import login_required, current_user

from app.modules.products import products
from app.modules.products.handlers import (
    create_seller_product, get_seller_products,
    get_all_product_categories, update_product, delete_product,
    get_product_by_guid
)


@products.route('', methods=['GET'])
@login_required
def index():
    if not current_user.sellers:
        return redirect(url_for('home.index'))

    page = request.args.get('page', 1, type=int)

    seller_products_pagination = get_seller_products(
        current_user.sellers[0].id, current_user.sellers[0].show_soldout_products, page=page
    )
    return render_template(
        'products/index.html',
        paginated_products=seller_products_pagination,
        section='your_products'
    )


@products.route('/<product_guid>', methods=['GET', 'PUT'])
@login_required
def manage_product(product_guid: str):
    if not current_user.sellers:
        return redirect(url_for('home.index'))

    try:
        product_guid = UUID(product_guid)
        product = get_product_by_guid(product_guid)
        if not product:
            return abort(404)
        if product.owner_seller_id != current_user.sellers[0].id:
            return abort(403)

        if request.method == 'PUT':
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))
            categories = request.form.getlist('categories')
            description = request.form.get('description')
            if not price and not stock and not categories and not description:
                return 'No data to update', 400

            update_product(product, price, stock, categories, description)
            return redirect(url_for('products.index'))

        # request.method == 'GET'
        return render_template(
            'products/[guid].html', product=product,
            product_categories=[c.name for c in product.categories],
            categories=[c.name for c in get_all_product_categories()],
            is_seller_product=True,
            section='your_products'
        )
    except ValueError:
        return redirect(url_for('products.index'))


@products.route('/<product_guid>/delete', methods=['POST'])
@login_required
def delete_seller_product(product_guid: str):
    if not current_user.sellers:
        return redirect(url_for('home.index'))

    product_guid = UUID(product_guid)
    product = get_product_by_guid(product_guid)

    delete_product(product)
    return redirect(url_for('products.index'))


@products.route('/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if not current_user.sellers:
        return redirect(url_for('home.index'))

    if request.method == 'POST':
        seller_id = current_user.sellers[0].id
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        categories = request.form.getlist('categories')
        description = request.form.get('description')
        brand = request.form.get('brand')
        is_second_hand = request.form.get('is_second_hand') == 'on'

        create_seller_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        return redirect(url_for('products.index'))

    #  request.method == 'GET'
    categories = get_all_product_categories()
    return render_template('products/create.html', categories=[c.name for c in categories], section='your_products')


@products.route('/shop')
def shop_products():
    all_products = index()
    return render_template('products/shop.html', products=all_products, section='shop')
