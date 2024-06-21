from datetime import timedelta, datetime
from enum import Enum
from typing import List
from uuid import UUID

import pytz
from flask_sqlalchemy.pagination import QueryPagination

from app.modules.carts.models import Cart, ProductReservation, CartStatus
from app.modules.orders.models import BuyerOrder, BuyersOrderStatus, SellerOrder, OrderedProduct, OrderReport
from app.modules.shared.consts import created_orders_ttl, page_size
from app.modules.shipments.handlers import create_shipment
from app.modules.shipments.models import Shipment
from extensions import db


def get_buyer_orders_by_buyer(buyer_id: int, page: int = 1, per_page: int = page_size) -> QueryPagination:
    """
    Get buyer orders by buyer id.
    :param buyer_id: the id of the buyer
    :param page: the page number to retrieve
    :param per_page: the number of items per page
    :return: the buyer orders
    """

    return (BuyerOrder.query
            .join(BuyerOrder.cart)
            .filter(Cart.owner_buyer_id == buyer_id, BuyerOrder.deleted_at.is_(None))
            .order_by(BuyerOrder.created_at.desc())
            .paginate(page=page, per_page=per_page))


def get_buyer_order_by_guid(guid: UUID, buyer_id: int) -> BuyerOrder | None:
    """
    Get buyer order by guid
    :param buyer_id: the buyer id
    :param guid: the guid of the buyer order
    :return: the buyer order
    """

    return BuyerOrder.query.filter(BuyerOrder.guid == guid and BuyerOrder.cart.owner_buyer_id == buyer_id).first()


def get_seller_order_by_guid(guid: UUID, seller_id: int) -> SellerOrder | None:
    """
    Get seller order by guid and seller_id
    :param guid: the guid of the seller order
    :param seller_id: the seller id
    :return: the seller order
    """

    return SellerOrder.query.filter_by(guid=guid, seller_id=seller_id).first()


def get_seller_orders_by_seller(seller_id: int, page: int = 1, per_page: int = page_size) -> QueryPagination:
    """
    Get seller orders by seller id.
    :param seller_id: the id of the seller
    :param page: the page number to retrieve
    :param per_page: the number of items per page
    :return: the seller orders
    """

    return (SellerOrder.query
            .filter_by(seller_id=seller_id, shipment=None)
            .order_by(SellerOrder.created_at.desc())
            .paginate(page=page, per_page=per_page))


def get_ordered_products_by_product(product_id: int, page: int = 1, per_page: int = page_size) -> QueryPagination:
    """
    Get ordered products by product id.
    :param product_id: the id of the product
    :param page: the page number to retrieve
    :param per_page: the number of items per page
    :return: the ordered products
    """

    return (OrderedProduct.query
            .filter_by(product_id=product_id)
            .order_by(OrderedProduct.created_at)
            .paginate(page=page, per_page=per_page))


class OrderCreationErrorReason(Enum):
    """
    Represents the reason of an order creation error.
    """

    INVALID_PRODUCTS = "invalid_products"
    LOCKED_PRODUCTS = "locked_products"
    ALREADY_CREATED = "already_created"


def create_buyer_order(cart: Cart) -> (
    BuyerOrder | None, List[ProductReservation] | None, OrderCreationErrorReason | None
):
    """
    Create a buyer order from a cart. If the order is already created, return None.
    :param cart: the cart
    :return: the buyer order, the invalid reservations and the error reason
    """

    # check already created order
    if BuyerOrder.query.filter_by(cart=cart, deleted_at=None).first():
        return None, None, OrderCreationErrorReason.ALREADY_CREATED

    reservations = [r for r in cart.reservations if r.deleted_at is None]

    # check invalid products
    invalid_reservations = [
        r for r in reservations if r.product.sequence != r.product_sequence
    ]
    if invalid_reservations:
        for r in invalid_reservations:
            r.deleted_at = db.func.now()
            # TODO: should create a new reservation?
        return None, invalid_reservations, OrderCreationErrorReason.INVALID_PRODUCTS

    # check locked products
    locked_reservations = [
        r for r in reservations if r.product.locked_stock > 0
    ]
    if locked_reservations:
        return None, locked_reservations, OrderCreationErrorReason.LOCKED_PRODUCTS

    # lock products
    for r in reservations:
        r.product.locked_stock += r.quantity

    total_currency = reservations[0].product.currency
    total_price = sum([r.product.price * r.quantity for r in reservations])

    # create order
    buyer_order = BuyerOrder(cart=cart, total_price=total_price, total_currency=total_currency)
    db.session.add(buyer_order)
    db.session.commit()
    return buyer_order, None, None


def complete_buyer_order(buyer_order: BuyerOrder) -> (BuyerOrder | None, List[SellerOrder] | None):
    """
    Complete buyer order. If the order is expired, delete it.
    :param buyer_order: the buyer order
    :return: the buyer order and the seller orders
    """

    if buyer_order.created_at.replace(tzinfo=pytz.UTC) < datetime.now(pytz.UTC) - timedelta(seconds=created_orders_ttl):
        for r in buyer_order.cart.reservations:
            r.product.locked_stock -= r.quantity
        buyer_order.deleted_at = db.func.now()
        db.session.commit()
        return None, None

    buyer_order.status = BuyersOrderStatus.COMPLETED
    buyer_order.cart.status = CartStatus.FINALIZED

    reservations = [r for r in buyer_order.cart.reservations if r.deleted_at is None]

    # unlock products and update stock
    for r in reservations:
        r.product.locked_stock -= r.quantity
        r.product.stock -= r.quantity

    # create seller orders
    seller_orders = []
    order_reports = []

    for r in reservations:
        ordered_product = OrderedProduct(product=r.product, quantity=r.quantity)

        # find seller order
        seller_order = None
        for so in seller_orders:
            if so.seller_id == r.product.owner_seller_id:
                seller_order = so
                break

        if not seller_order:
            seller_order = SellerOrder(buyer_order=buyer_order, seller_id=r.product.owner_seller_id)
            db.session.add(seller_order)
            seller_orders.append(seller_order)

        seller_order.ordered_products.append(ordered_product)

    db.session.commit()
    # create order reports
    for so in seller_orders:
        order_report = OrderReport(buyer_order=buyer_order, buyer=buyer_order.cart.buyer,
                                   seller=so.seller, seller_order=so)
        db.session.add(order_report)
        order_reports.append(order_report)
    db.session.commit()
    return buyer_order, seller_orders


def complete_seller_orders(seller_orders: List[UUID], seller_id: int) -> Shipment | None:
    """
    Complete seller orders
    :param seller_id: the seller id
    :param seller_orders: the list of seller orders
    :return:
    """

    orders = SellerOrder.query.filter(SellerOrder.guid.in_(seller_orders), SellerOrder.seller_id == seller_id).all()
    if not orders:
        return None
    return create_shipment(orders, seller_id)
