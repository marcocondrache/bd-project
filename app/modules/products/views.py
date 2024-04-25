from flask import request, render_template, url_for, redirect
from flask_login import login_required, current_user

from app.modules.products import products
from app.modules.products.handlers import create_product, get_products, get_seller_products, get_all_product_categories


@products.route('', methods=['GET'])
@login_required
def user_products():
    if not current_user.sellers:
        return redirect(url_for('home.index'))
    
    page = request.args.get('page', 1, type=int)
    seller_products = get_seller_products(current_user.sellers[0].id, page=page)

    return render_template('products/index.html', products=seller_products)


@products.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        if not current_user.sellers:
            return {'message': 'not a seller'}, 403
        seller_id = current_user.sellers[0].id
        name = request.form.get('name')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        categories = request.form.getlist('categories')
        description = request.form.get('description')
        brand = request.form.get('brand')
        is_second_hand = request.form.get('is_second_hand') == 'on'

        create_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        return redirect(url_for('products.user_products'))
    
    categories = get_all_product_categories()
    return render_template('products/create.html', categories=[c.to_json() for c in categories])


@products.route('/<int:product_id>', methods=['GET'])
def get_product(product_id: int):
    # TODO: Implement product view
    return str(product_id)


@products.route('/shop')
def shop_products():
    all_products = get_products()
    return render_template('products/shop.html', products=all_products)
