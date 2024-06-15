from typing import List

from flask_sqlalchemy.pagination import QueryPagination

from app.modules.orders.models import SellerOrder, SellerOrderStatus
from app.modules.shared.consts import page_size
from app.modules.shipments.models import Shipment, ShipmentStatus
from extensions import db


def create_shipment(seller_orders: List[SellerOrder]) -> Shipment:
    """
    Create a shipment for the given seller orders.
    :param seller_orders: the seller orders
    :return: the created shipment
    """

    shipment = Shipment()
    shipment.current_status = ShipmentStatus.ACCEPTED
    shipment.orders = seller_orders
    db.session.add(shipment)

    for seller_order in seller_orders:
        if seller_order.status != SellerOrderStatus.CREATED:
            raise ValueError("All seller orders must be created to create a shipment")

        seller_order.shipment = shipment
        seller_order.status = SellerOrderStatus.COMPLETED
        db.session.add(seller_order)

    db.session.commit()
    return shipment


def get_shipments_by_seller(seller_id: int, page: int = 1, per_page: int = page_size) -> QueryPagination:
    """
    Get shipments by seller id.
    :param seller_id: the id of the seller
    :param page: the page number to retrieve
    :param per_page: the number of items per page
    :return: the shipments
    """

    return (Shipment.query
            .join(Shipment.orders)
            .filter(SellerOrder.seller_id == seller_id)
            .order_by(Shipment.created_at.desc())
            .paginate(page=page, per_page=per_page))
