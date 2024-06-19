from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.products.models import Product
    from app.modules.orders.models import SellerOrder
    from app.modules.buyers.models import Buyer
else:
    Product = "Product"
    SellerOrder = "SellerOrder"
    Buyer = "Buyer"

from extensions import db
import uuid


class ProductReviewHistory(db.Model):
    """
    Product review history model
    Represents a history of a review of a product by a buyer. Contains a rating and a message.
    """
    __tablename__ = "product_review_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    product_review_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("product_reviews.id"), nullable=False)

    rating: Mapped[int] = mapped_column(db.Integer, nullable=False)
    message: Mapped[str] = mapped_column(db.String(255), nullable=False)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())


class ProductReview(db.Model):
    """
    Product review model
    Represents a review of a product by a buyer. Contains a rating and a message.
    """
    __tablename__ = "product_reviews"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    seller_order_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("seller_orders.id"), nullable=False)
    buyer_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("buyers.id"), nullable=False)

    current_rating: Mapped[int] = mapped_column(db.Integer, nullable=False)
    current_message: Mapped[str] = mapped_column(db.String(255), nullable=False)

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now())
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    product: Mapped[Product] = db.relationship("Product", back_populates="reviews")
    seller_order: Mapped[SellerOrder] = db.relationship("SellerOrder", back_populates="reviews")
    buyer: Mapped[Buyer] = db.relationship("Buyer", back_populates="reviews")
    history: Mapped[ProductReviewHistory] = db.relationship("ProductReviewHistory", back_populates="product_review")
