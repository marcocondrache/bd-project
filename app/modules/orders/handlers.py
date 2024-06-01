from enum import Enum
from typing import List
from uuid import UUID

from flask_sqlalchemy.pagination import QueryPagination

from app.modules.carts.models import Cart, ProductReservation, CartStatus
from app.modules.orders.models import BuyerOrder, BuyersOrderStatus, SellerOrder, OrderedProduct
from extensions import db


def get_buyer_orders_by_buyer(buyer_id: int, page: int = 1, per_page: int = 20) -> QueryPagination:
    # TODO: clean locks
    return (BuyerOrder.query
            .join(BuyerOrder.cart)
            .filter(Cart.owner_buyer_id == buyer_id, BuyerOrder.deleted_at.is_(None))
            .order_by(BuyerOrder.created_at)
            .paginate(page=page, per_page=per_page))


def get_buyer_order_by_guid(guid: UUID) -> BuyerOrder | None:
    return BuyerOrder.query.filter_by(guid=guid).first()


def get_seller_orders_by_seller(seller_id: int, page: int = 1, per_page: int = 20) -> QueryPagination:
    return (SellerOrder.query
            .filter_by(seller_id=seller_id)
            .order_by(SellerOrder.created_at)
            .paginate(page=page, per_page=per_page))


def get_ordered_products_by_product(product_id: int, page: int = 1, per_page: int = 20) -> QueryPagination:
    return (OrderedProduct.query
            .filter_by(product_id=product_id)
            .order_by(OrderedProduct.created_at)
            .paginate(page=page, per_page=per_page))


class OrderCreationErrorReason(Enum):
    INVALID_PRODUCTS = "invalid_products"
    LOCKED_PRODUCTS = "locked_products"
    ALREADY_CREATED = "already_created"


def create_buyer_order(cart: Cart) -> (
    BuyerOrder | None, List[ProductReservation] | None, OrderCreationErrorReason | None
):
    # TODO: clean locks

    # check already created order
    if BuyerOrder.query.filter_by(cart=cart).first():
        return None, None, OrderCreationErrorReason.ALREADY_CREATED

    reservations = [r for r in cart.reservations if r.deleted_at is None]

    # check invalid products
    invalid_reservations = [
        r for r in reservations if r.product.sequence != r.product_sequence
    ]
    if invalid_reservations:
        return None, invalid_reservations, OrderCreationErrorReason.INVALID_PRODUCTS

    # check locked products
    # TODO: check if r.product.stock - r.locked.stock >= r.quantity (?)
    locked_reservations = [
        r for r in reservations if r.product.locked_stock > 0
    ]
    if locked_reservations:
        return None, locked_reservations, OrderCreationErrorReason.LOCKED_PRODUCTS

    # lock products
    for r in reservations:
        r.product.locked_stock += r.quantity

    # create order
    buyer_order = BuyerOrder(cart=cart)
    db.session.add(buyer_order)
    db.session.commit()
    return buyer_order, None, None


def complete_buyer_order(buyer_order: BuyerOrder) -> (BuyerOrder | None, List[SellerOrder] | None):
    # TODO check timeout

    buyer_order.status = BuyersOrderStatus.COMPLETED
    buyer_order.cart.status = CartStatus.FINALIZED

    reservations = [r for r in buyer_order.cart.reservations if r.deleted_at is None]

    # unlock products and update stock
    for r in reservations:
        r.product.locked_stock -= r.quantity
        r.product.stock -= r.quantity

    # create seller orders
    seller_orders = []
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
    return buyer_order, seller_orders
