from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, List

from extensions import db

if TYPE_CHECKING:
    from app.modules.users.models import User
    from app.modules.products.models import Product
else:
    User = "User"
    Product = "Product"


class Seller(db.Model):
    __tablename__ = "sellers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    iban: Mapped[str] = mapped_column("current_iban", db.String(255), nullable=False)
    show_soldout_products: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)

    user: Mapped[User] = db.relationship("User", back_populates="sellers")
    products: Mapped[List[Product]] = db.relationship("Product", back_populates="seller")

    def __repr__(self):
        return f"<Seller user={self.user.email} iban={self.iban} show_soldout_products={self.show_soldout_products}>"
