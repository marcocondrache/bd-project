import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db

if TYPE_CHECKING:
    from app.modules.carts.models import Cart
    from app.modules.products.models import Product
    from app.modules.sellers.models import Seller
else:
    Cart = "Cart"
    Product = "Product"
    Seller = "Seller"


class BuyersOrderStatus(Enum):
    CREATED = "created"
    COMPLETED = "completed"

    def __str__(self):
        return self.value.capitalize()


class BuyerOrder(db.Model):
    __tablename__ = "buyers_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    cart_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    status: Mapped[BuyersOrderStatus] = mapped_column(
        "current_status", db.Enum(BuyersOrderStatus), nullable=False, default=BuyersOrderStatus.CREATED
    )

    created_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at: Mapped[datetime] = mapped_column(db.DateTime, nullable=True)

    cart: Mapped[Cart] = db.relationship("Cart", back_populates="buyer_orders")
    seller_orders: Mapped[List["SellerOrder"]] = db.relationship("SellerOrder", back_populates="buyer_order")

    def __repr__(self):
        return (f"<BuyerOrder guid={self.guid} status={self.status} cart_id={self.cart_id} "
                f"created_at={self.created_at} updated_at={self.updated_at} deleted_at={self.deleted_at}>")


class SellerOrderStatus(Enum):
    CREATED = "created"
    COMPLETED = "completed"


class SellerOrder(db.Model):
    __tablename__ = "sellers_orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    buyer_order_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("buyers_orders.id"), nullable=False)
    seller_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    status: Mapped[SellerOrderStatus] = mapped_column(
        "current_status", db.Enum(SellerOrderStatus), nullable=False, default=SellerOrderStatus.CREATED
    )
    # TODO when shipment is implemented
    # shipment_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("shipments.id"), nullable=False)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )

    buyer_order: Mapped[BuyerOrder] = db.relationship("BuyerOrder", back_populates="seller_orders")
    seller: Mapped[Seller] = db.relationship("Seller", back_populates="orders")
    ordered_products: Mapped[List["OrderedProduct"]] = db.relationship(
        "OrderedProduct", back_populates="seller_order"
    )

    def __repr__(self):
        return (f"<SellerOrder guid={self.guid} status={self.status} buyer_order_id={self.buyer_order_id} "
                f"created_at={self.created_at} updated_at={self.updated_at}>")


class OrderedProduct(db.Model):
    __tablename__ = "ordered_products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    sellers_order_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("sellers_orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(db.Integer, nullable=False)

    product: Mapped[Product] = db.relationship("Product", back_populates="ordered_products")
    seller_order: Mapped[SellerOrder] = db.relationship("SellerOrder", back_populates="ordered_products")

    def __repr__(self):
        return (f"<OrderedProduct id={self.id} sellers_order_id={self.sellers_order_id} product_id={self.product_id} "
                f"quantity={self.quantity}>")
