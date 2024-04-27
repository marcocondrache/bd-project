from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column

from extensions import db

if TYPE_CHECKING:
    from app.modules.buyers.models import Buyer
else:
    Buyer = "Buyer"


class CartStatus(Enum):
    ACTIVE = "active"
    FINALIZED = "finalized"


class ProductReservation(db.Model):
    __tablename__ = "product_reservations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    cart_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("carts.id"), nullable=False)

    product_sequence: Mapped[int] = mapped_column(db.Integer, nullable=False)
    quantity: Mapped[int] = mapped_column("current_quantity", db.Integer, nullable=False)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    product = db.relationship("Product")
    cart = db.relationship("Cart", back_populates="reservations")

    def __repr__(self):
        return (f"<ProductReservation id={self.id} product_id={self.product_id} cart_id={self.cart_id}"
                f"product_sequence={self.product_sequence} quantity={self.quantity} created_at={self.created_at}>"
                f"updated_at={self.updated_at} deleted_at={self.deleted_at}>")


# TODO: Implement the Cart history model


class Cart(db.Model):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    guid: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    owner_buyer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("buyers.id"), nullable=False)

    status: Mapped[CartStatus] = mapped_column(db.Enum(CartStatus), nullable=False, default=CartStatus.ACTIVE)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    buyer: Mapped[Buyer] = db.relationship("Buyer", back_populates="carts")
    reservations: Mapped[List[ProductReservation]] = db.relationship("ProductReservation", back_populates="cart")

    def __repr__(self):
        return f"<Cart id={self.id} user_id={self.user_id} created_at={self.created_at} updated_at={self.updated_at}>"
