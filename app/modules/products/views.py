from flask import request, render_template
from flask_login import login_required, current_user

from app.modules.products import products
from app.modules.products.handlers import create_product, get_products


@products.route('', methods=['GET', 'POST'])
@login_required
def user_products():
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

        product = create_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        if not product:
            return {'message': 'seller not found'}, 404

        return {'message': 'product created'}, 200

    return render_template('products/index.html')


@products.route('/<int:product_id>', methods=['GET'])
def product(product_id: int):
    return str(product_id)


@products.route("/shop")
def shop_products():
    all_products = get_products()
    return render_template('products/shop.html', products=all_products)
