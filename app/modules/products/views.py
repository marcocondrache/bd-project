from flask_login import login_required, current_user
from flask import request, render_template

from app.modules.products import products
from app.modules.products.handlers import create_product


@products.route('', methods=['GET', 'POST'])
@login_required
def user_products():
    if request.method == 'POST':
        seller_id = current_user.id
        name = request.json.get('name')
        price = request.json.get('price')
        stock = request.json.get('stock')
        categories = request.json.get('categories')
        description = request.json.get('description')
        brand = request.json.get('brand')
        is_second_hand = request.json.get('is_second_hand')

        product = create_product(seller_id, name, price, stock, categories, description, brand, is_second_hand)
        if not product:
            return {'message': 'seller not found'}, 404

        return {'message': 'product created'}, 200
    return render_template('products/index.html')
