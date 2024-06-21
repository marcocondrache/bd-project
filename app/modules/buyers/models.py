from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, List

from extensions import db

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.carts.models import Cart
    from app.modules.products.models import ProductReview
    from app.modules.orders.models import OrderReport
else:
    User = "User"
    Cart = "Cart"
    ProductReview = "ProductReview"
    OrderReport = "OrderReport"


class Buyer(db.Model):
    __tablename__ = "buyers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    destination_address: Mapped[str] = mapped_column("current_destination_address", db.String(255), nullable=False)
    card_number: Mapped[str] = mapped_column("current_card_number", db.String(255), nullable=False)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    user: Mapped[User] = db.relationship("User", back_populates="buyers")
    carts: Mapped[List[Cart]] = db.relationship("Cart", back_populates="buyer")

    reviews: Mapped[List[ProductReview]] = db.relationship("ProductReview", back_populates="buyer")
    order_reports: Mapped[List[OrderReport]] = db.relationship("OrderReport", back_populates="buyer")

    def __repr__(self):
        return (f"<Buyer user={self.user.email} destination_address={self.destination_address} "
                f"card_number={self.card_number}>")
