from uuid import UUID

from flask import request, render_template, url_for, redirect, abort
from flask_login import login_required, current_user

from app.modules.carts import carts
from app.modules.carts.handlers import get_cart_by_buyer, update_cart, remove_from_cart, get_cart_products
from app.modules.products.handlers import (
    get_product_by_guid
)


def authorize_buyer():
    if not current_user.buyers:
        return redirect(url_for('home.index_view'))


def validate_product(product_guid: str):
    try:
        product_guid = UUID(product_guid)
        product = get_product_by_guid(product_guid)
        if not product:
            return abort(404)
        return product
    except ValueError:
        return redirect(url_for('products.index_view'))


@carts.route('', methods=['GET'])
@login_required
def index_view():
    authorize_buyer()

    buyer_id = current_user.buyers[0].id

    # TODO: add pagination
    cart = get_cart_by_buyer(buyer_id)  # should use "get_cart_or_create"?
    products = get_cart_products(cart)
    return render_template(
        'carts/index.html',
        cart=cart,
        reservations=cart.reservations if cart else [],
        section='your_cart'
    )


@carts.route('/<product_guid>/update', methods=['POST'])
@login_required
def cart_update_view(product_guid: str):
    authorize_buyer()

    buyer_id = current_user.buyers[0].id
    product = validate_product(product_guid)
    quantity = int(request.json.get('quantity', 1))

    cart, product = update_cart(buyer_id, product, quantity)
    if product:
        return product.to_json(), 400

    return '', 200


@carts.route('/<product_guid>/delete', methods=['POST'])
@login_required
def cart_delete_view(product_guid: str):
    authorize_buyer()

    buyer_id = current_user.buyers[0].id
    product = validate_product(product_guid)

    remove_from_cart(buyer_id, product)

    return redirect(url_for('carts.index_view'))
