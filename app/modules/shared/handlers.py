from app.modules.orders.models import BuyerOrder, BuyersOrderStatus
from app.modules.shared.consts import created_orders_ttl
from extensions import db


def clean_expired_orders() -> bool:
    """ remove the buyer orders with status "created" whose creation time is older than timeout and unlock the
    products"""
    invalid_locks = (
        BuyerOrder.query
        .filter_by(status=BuyersOrderStatus.CREATED, deleted_at=None)
        .filter(
            BuyerOrder.created_at < db.func.now() - db.func.make_interval(0, 0, 0, 0, 0, 0, created_orders_ttl))
        .all()
    )

    for order in invalid_locks:
        # unlock products
        for r in order.cart.reservations:
            r.product.locked_stock -= r.quantity

        # delete order
        order.deleted_at = db.func.now()

    if invalid_locks:
        db.session.commit()

    return bool(invalid_locks)
