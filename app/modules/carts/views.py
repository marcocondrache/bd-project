from uuid import UUID

from flask import request, render_template, abort, flash
from flask_login import login_required, current_user

from app.modules.carts import carts
from app.modules.carts.handlers import get_cart_by_buyer, update_cart, remove_from_cart, get_reservation_by_cart
from app.modules.products.handlers import (
    get_product_by_guid
)
from app.modules.products.models import Product
from app.modules.shared.utils import buyer_required


def validate_product(product_guid: str) -> Product:
    """
    Utility function to validate a product by its guid.
    :param product_guid: the guid of the product
    :return: the product if it exists, otherwise abort with a 404 error
    """
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
@buyer_required
def index_view():
    """
    Cart view.
    :return: The cart view.
    """
    buyer_id = current_user.buyers[0].id

    # handling form submission
    if request.method == 'POST':
        product_guid = request.form.get('product_guid')
        quantity = int(request.form.get('quantity'))

        product = validate_product(product_guid)

        # delete product from cart
        if quantity < 1:
            remove_from_cart(buyer_id, product)

        # update quantity
        else:
            cart, product = update_cart(buyer_id, product, quantity)
            if product:
                flash(f"Someone bought this product or the seller changed it. Please try again", 'danger')

    page = request.args.get('page', 1, type=int)

    cart = get_cart_by_buyer(buyer_id)

    # get the reservations of the cart
    reservations = get_reservation_by_cart(cart, page)
    return render_template(
        'carts/index.html',
        cart=cart,
        paginated_reservations=reservations
    )
