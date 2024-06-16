from typing import List
from uuid import UUID

from flask import render_template, url_for, redirect, abort, flash, request
from flask_login import login_required, current_user

from app.modules.carts.handlers import get_cart_by_buyer
from app.modules.orders import orders
from app.modules.orders.handlers import (
    create_buyer_order, OrderCreationErrorReason, get_buyer_order_by_guid,
    complete_buyer_order, get_buyer_orders_by_buyer, get_seller_orders_by_seller,
    get_seller_order_by_guid, complete_seller_orders
)
from app.modules.shared.utils import buyer_required, seller_required


@orders.route('', methods=['GET'])
@login_required
@buyer_required
def index_view():
    """
    Shows the buyer orders. The user must be a buyer.
    :return: The orders view.
    """

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
    """
    Shows the seller orders. The user must be a seller.
    :return: The seller orders view.
    """

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
    """
    Creates an order. The user must be a buyer.
    :return: A redirect to the order view.
    """

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
    """
    Completes an order. The user must be a buyer.
    :param order_guid: The guid of the order to complete.
    :return: A redirect to the home view.
    """

    buyer_order = get_buyer_order_by_guid(order_guid, current_user.buyers[0].id)
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


@orders.route('/<uuid:order_guid>/details', methods=['GET'])
@login_required
@buyer_required
def order_details_view(order_guid: UUID):
    """
    Shows the details of an order. The user must be a buyer.
    :param order_guid: The guid of the order.
    :return: The order details view.
    """

    buyer_order = get_buyer_order_by_guid(order_guid, current_user.buyers[0].id)
    if not buyer_order:
        abort(404)

    def map_history(history):
        for h in history:
            h.created_at = h.created_at.strftime("%Y-%m-%d %H:%M:%S")
            h.status = h.status.value
        return history

    shipment_history = {so.seller: map_history(so.shipment.history) for so in buyer_order.seller_orders if so.shipment}

    return render_template(
        'orders/buyer_order_info.html',
        order=buyer_order,
        shipment_history=shipment_history,
    )


@orders.route('/incoming/<uuid:seller_order_guid>/details', methods=['GET'])
@login_required
@seller_required
def seller_order_details_view(seller_order_guid: UUID):
    """
    Shows the details of a seller order. The user must be a seller.
    :param seller_order_guid: The guid of the seller order.
    :return: The seller order details view.
    """

    seller_order = get_seller_order_by_guid(seller_order_guid, current_user.sellers[0].id)
    if not seller_order:
        abort(404)

    return render_template(
        'orders/seller_order_info.html',
        order=seller_order,
    )


@orders.route('/incoming/complete', methods=['POST'])
@login_required
@seller_required
def complete_seller_order_view():
    """
    Completes a seller order. The user must be a seller.
    :return: A redirect to the seller orders view.
    """

    order_guids = request.json['order_guids']
    seller_order = complete_seller_orders(order_guids)
    if not seller_order:
        flash("Some orders are not valid", "danger")
        return redirect(url_for('orders.seller_orders_view'))

    return redirect(url_for('orders.seller_orders_view'))
