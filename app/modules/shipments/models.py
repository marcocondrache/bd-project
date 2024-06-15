from __future__ import annotations

import enum

from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, List
from sqlalchemy.dialects.postgresql import UUID

from extensions import db
import uuid

if TYPE_CHECKING:
    from app.modules.orders.models import SellerOrder
else:
    SellerOrder = "SellerOrder"


class ShipmentStatus(enum.Enum):
    """
    Represents the status of a shipment.
    """

    ACCEPTED = "ACCEPTED"
    SHIPPED = "SHIPPED"
    IN_DELIVERY = "IN_DELIVERY"
    DELIVERED = "DELIVERED"

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

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    orders: Mapped[List[SellerOrder]] = db.relationship("SellerOrder", back_populates="shipment")

    def __repr__(self):
        return f"<Shipment guid={self.guid} current_status={self.current_status}>"

    def to_json(self):
        return {
            "guid": self.guid,
            "current_status": self.current_status,
        }
