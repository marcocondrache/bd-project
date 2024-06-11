from uuid import UUID

from flask import render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user

from app.modules.carts.handlers import get_cart_by_buyer
from app.modules.orders import orders
from app.modules.orders.handlers import (
    create_buyer_order, OrderCreationErrorReason, get_buyer_order_by_guid,
    complete_buyer_order, get_buyer_orders_by_buyer, get_seller_orders_by_seller
)
from app.modules.shared.utils import buyer_required, seller_required


@orders.route('', methods=['GET'])
@login_required
@buyer_required
def index_view():
    buyer_id = current_user.buyers[0].id

    from app.modules.shared.handlers import clean_expired_orders
    if clean_expired_orders():
        flash("Some orders expired", "warning")

    page = request.args.get('page', 1, type=int)
    paginated_orders = get_buyer_orders_by_buyer(buyer_id, page)
    return render_template(
        'orders/index.html',
        paginated_orders=paginated_orders
    )


@orders.route('/incoming', methods=['GET'])
@login_required
@seller_required
def seller_orders_view():
    seller_id = current_user.sellers[0].id

    page = request.args.get('page', 1, type=int)
    paginated_orders = get_seller_orders_by_seller(seller_id, page)
    return render_template(
        'orders/seller_orders.html',
        paginated_orders=paginated_orders
    )


@orders.route('/create', methods=['GET'])
@login_required
@buyer_required
def create_order_view():
    buyer_id = current_user.buyers[0].id

    from app.modules.shared.handlers import clean_expired_orders
    clean_expired_orders()

    cart = get_cart_by_buyer(buyer_id)
    (order, invalid_reservations, error_reason) = create_buyer_order(cart)

    if error_reason == OrderCreationErrorReason.ALREADY_CREATED:
        flash("Order already created", "danger")
        return redirect(url_for('carts.index_view'))

    if error_reason == OrderCreationErrorReason.INVALID_PRODUCTS:
        flash(f"Someone products has been bought or the seller changed it. Please try again", 'danger')
        return redirect(url_for('carts.index_view'))

    if error_reason == OrderCreationErrorReason.LOCKED_PRODUCTS:
        flash("An order is already in progress for this products. Please try again later.", "danger")
        return redirect(url_for('carts.index_view'))

    return redirect(url_for('orders.complete_order_view', order_guid=order.guid))


@orders.route('/<uuid:order_guid>/complete', methods=['POST', 'GET'])
@login_required
@buyer_required
def complete_order_view(order_guid: UUID):
    buyer_order = get_buyer_order_by_guid(order_guid)
    if not buyer_order:
        abort(404)

    if request.method == 'POST':
        (buyer_order, seller_orders) = complete_buyer_order(buyer_order)

        if not buyer_order:
            flash("Order expired", "danger")
            return redirect(url_for('carts.index_view'))

        return redirect(url_for('home.index_view'))

    return render_template(
        'orders/complete_order.html',
        order=buyer_order,
    )


@orders.route('/orders/<uuid:order_guid>/details', methods=['GET'])
@login_required
@buyer_required
def order_details_view(order_guid: UUID):
    buyer_order = get_buyer_order_by_guid(order_guid)
    if not buyer_order:
        abort(404)

    return render_template(
        'orders/buyer_order_info.html',
        order=buyer_order,
    )
