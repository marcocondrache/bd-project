from uuid import UUID

from flask import request, render_template, url_for, redirect, abort, flash
from flask_login import login_required, current_user

from app.modules.carts import carts
from app.modules.carts.handlers import get_cart_by_buyer, update_cart, remove_from_cart, get_reservation_by_cart
from app.modules.products.handlers import (
    get_product_by_guid
)
from app.modules.products.models import Product


def authorize_buyer():
    if not current_user.buyers:
        return redirect(url_for('home.index_view'))


def validate_product(product_guid: str) -> Product:
    try:
        product_guid = UUID(product_guid)
        product = get_product_by_guid(product_guid)
        if not product:
            abort(404)
        return product
    except ValueError:
        abort(400)


@carts.route('', methods=['GET', 'POST'])
@login_required
def index_view():
    authorize_buyer()

    buyer_id = current_user.buyers[0].id

    if request.method == 'POST':
        product_guid = request.form.get('product_guid')
        product = validate_product(product_guid)

        quantity = int(request.form.get('quantity'))
        # delete product from cart
        if quantity < 1:
            remove_from_cart(buyer_id, product)

        # update quantity
        else:
            cart, product = update_cart(buyer_id, product, quantity)
            if product:
                flash(f"Product {product.name} is no longer available... smth like that", 'danger')

    page = request.args.get('page', 1, type=int)

    cart = get_cart_by_buyer(buyer_id)
    reservations = get_reservation_by_cart(cart, page)
    return render_template(
        'carts/index.html',
        cart=cart,
        paginated_reservations=reservations,
        section='your_cart'
    )
