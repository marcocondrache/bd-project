from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING

from extensions import db

if TYPE_CHECKING:
    from app.modules.sellers.models import Seller
else:
    Seller = "Seller"


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    owner_seller_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("sellers.id"), nullable=False)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=True)
    brand: Mapped[str] = mapped_column(db.String(255), nullable=True)
    is_second_hand: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=False)
    sequence: Mapped[int] = mapped_column("current_sequence", db.Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column("current_price", db.Float, nullable=False)
    currency: Mapped[str] = mapped_column("current_currency", db.String(3), nullable=False)
    stock: Mapped[int] = mapped_column("current_stock", db.Integer, nullable=False)
    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    seller: Mapped["Seller"] = db.relationship("Seller", back_populates="products")

    def __repr__(self):
        return (f"<Product owner_seller_id={self.owner_seller_id} name={self.name} description={self.description} "
                f"brand={self.brand} is_second_hand={self.is_second_hand} sequence={self.sequence} price={self.price} "
                f"currency={self.currency} stock={self.stock}>")
