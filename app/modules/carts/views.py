from uuid import UUID

from flask import request, render_template, url_for, redirect, abort
from flask_login import login_required, current_user

from app.modules.carts import carts
from app.modules.carts.handlers import get_cart_by_buyer, update_cart, remove_from_cart
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


@carts.route('', methods=['GET', 'POST'])
@login_required
def index_view():
    authorize_buyer()

    buyer_id = current_user.buyers[0].id

    if request.method == 'POST':
        product_guid = request.form.get('product_guid')
        product = validate_product(product_guid)

        quantity = int(request.form.get('quantity'))
        if quantity < 1:
            # delete product from cart
            remove_from_cart(buyer_id, product)
            cart = get_cart_by_buyer(buyer_id)
            return render_template(
                'carts/index.html',
                cart=cart,
                reservations=cart.get_active_reservations() if cart else [],
                section='your_cart'
            )
        # update quantity
        cart, product = update_cart(buyer_id, product, quantity)
        return render_template(
            'carts/index.html',
            cart=cart,
            reservations=cart.get_active_reservations() if cart else [],
            section='your_cart'
        )

    # TODO: add pagination
    cart = get_cart_by_buyer(buyer_id)  # should use "get_cart_or_create"?
    return render_template(
        'carts/index.html',
        cart=cart,
        reservations=cart.get_active_reservations() if cart else [],
        section='your_cart'
    )
