from typing import List

from flask_sqlalchemy.pagination import QueryPagination

from app.modules.orders.models import SellerOrder, SellerOrderStatus
from app.modules.shared.consts import DEFAULT_PAGE_SIZE
from app.modules.shipments.models import Shipment, ShipmentStatus
from extensions import db


def get_shipment_by_uuid(shipment_uuid: str, seller_id: int) -> Shipment:
    """
    Get a shipment by its UUID.
    :param seller_id: the id of the seller
    :param shipment_uuid: the UUID of the shipment
    :return: the requested shipment
    """

    return Shipment.query.filter_by(guid=shipment_uuid, seller_id=seller_id).first()


def create_shipment(seller_orders: List[SellerOrder], seller_id: int) -> Shipment:
    """
    Create a shipment for the given seller orders.
    :param seller_id: the id of the seller
    :param seller_orders: the orders related to the given seller
    :return: the created shipment
    """

    shipment = Shipment()
    shipment.current_status = ShipmentStatus.ACCEPTED
    shipment.orders = seller_orders
    shipment.seller_id = seller_id
    db.session.add(shipment)

    for seller_order in seller_orders:
        if seller_order.status != SellerOrderStatus.CREATED:
            raise ValueError("All seller orders must be created to create a shipment")

        seller_order.shipment = shipment
        seller_order.status = SellerOrderStatus.COMPLETED
        db.session.add(seller_order)

    db.session.commit()
    return shipment


def update_shipment_status(shipment: Shipment) -> Shipment:
    """
    Update the status of a shipment.
    :param shipment: the shipment to update
    :return: the updated shipment
    """

    next_status = shipment.current_status.get_next_status()

    shipment.current_status = next_status
    db.session.add(shipment)
    db.session.commit()
    return shipment


def get_shipments_by_seller(seller_id: int, page: int = 1, per_page: int = DEFAULT_PAGE_SIZE) -> QueryPagination:
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
