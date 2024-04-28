from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user

from app.modules.products import products
from app.modules.products.forms import SearchForm
from app.modules.products.handlers import create_product, get_seller_products, get_all_product_categories, \
    update_product, delete_product, get_products_by_keyword


@products.route('', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def manage_products():
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

        create_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        return redirect(url_for('products.manage_products'))

    if request.method == 'PUT':
        seller_id = current_user.sellers[0].id
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        categories = request.form.getlist('categories')
        description = request.form.get('description')
        if not price and not stock and not categories and not description:
            return 'No data to update', 400

        update_product(seller_id, price, stock, categories, description)
        return redirect(url_for('products.manage_products'))

    if request.method == 'DELETE':
        product_guid = request.form.get('product_guid')
        if not product_guid:
            return 'No product id provided', 400

        delete_product(current_user.sellers[0].id, product_guid)
        return redirect(url_for('products.manage_products'))

    #  request.method == 'GET'
    page = request.args.get('page', 1, type=int)

    seller_products_pagination = get_seller_products(
        current_user.sellers[0].id, current_user.sellers[0].show_soldout_products, page=page
    )
    return render_template('products/index.html', paginated_products=seller_products_pagination)


@products.route('/create', methods=['GET'])
@login_required
def product_creation():
    if not current_user.sellers:
        return redirect(url_for('home.index'))

    categories = get_all_product_categories()
    return render_template('products/create.html', categories=[c.to_json() for c in categories])


@products.route('/search', methods=['GET'])
@login_required
def search_products():
    search = SearchForm(request.args)

    if search.validate():
        query_key = search.search.data
        page = get_products_by_keyword(query_key, search.page.data)

        return render_template('products/list.html', page=page)

    return redirect(url_for('home.index'))
