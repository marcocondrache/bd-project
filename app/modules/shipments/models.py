from __future__ import annotations

import enum

from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, List
from sqlalchemy.dialects.postgresql import UUID

from extensions import db
import uuid

if TYPE_CHECKING:
    from app.modules.orders.models import SellerOrder
    from app.modules.sellers.models import Seller
else:
    SellerOrder = "SellerOrder"
    Seller = "Seller"


class ShipmentStatus(enum.Enum):
    """
    Represents the status of a shipment.
    """

    ACCEPTED = "ACCEPTED"
    SHIPPED = "SHIPPED"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"

    def get_next_status(self):
        if self == ShipmentStatus.ACCEPTED:
            return ShipmentStatus.SHIPPED
        if self == ShipmentStatus.SHIPPED:
            return ShipmentStatus.IN_DELIVERY
        if self == ShipmentStatus.IN_DELIVERY:
            return ShipmentStatus.DELIVERED
        return None

    def __str__(self):
        return self.value


class Shipment(db.Model):
    """
    Represents a shipment. A shipment is a collection of orders that are shipped together.
    All the orders in a shipment must be from the same seller.
    """

    __tablename__ = "shipments"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guid: Mapped[uuid.UUID] = db.Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    current_status: Mapped[ShipmentStatus] = db.Column(db.Enum(ShipmentStatus), nullable=False)
    seller_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    orders: Mapped[List[SellerOrder]] = db.relationship("SellerOrder", back_populates="shipment")
    history: Mapped[List["ShipmentHistory"]] = db.relationship("ShipmentHistory", back_populates="shipment")
    seller: Mapped["Seller"] = db.relationship("Seller", back_populates="shipments")

    def is_delivered(self):
        """
        Check if the shipment is delivered.
        :return:
        """
        return self.current_status == ShipmentStatus.DELIVERED

    def __repr__(self):
        return f"<Shipment guid={self.guid} current_status={self.current_status}>"

    def to_json(self):
        return {
            "guid": self.guid,
            "current_status": self.current_status,
        }


class ShipmentHistory(db.Model):
    """
    Represents the history of a shipment. This table is used to store the history of a shipment.
    """

    __tablename__ = "shipment_history"

    id: Mapped[int] = db.Column(db.Integer, primary_key=True, autoincrement=True)
    shipment_id: Mapped[int] = db.Column(db.Integer, db.ForeignKey("shipments.id"), nullable=False)
    status: Mapped[ShipmentStatus] = db.Column(db.Enum(ShipmentStatus), nullable=False)
    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())

    shipment: Mapped[Shipment] = db.relationship("Shipment", back_populates="history")

    def __repr__(self):
        return f"<ShipmentHistory shipment_id={self.shipment_id} status={self.status}>"
