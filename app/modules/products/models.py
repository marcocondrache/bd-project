from __future__ import annotations

from sqlalchemy import Table
from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING, List
from sqlalchemy.dialects.postgresql import UUID

from extensions import db
import uuid

from extensions import Base

if TYPE_CHECKING:
    from app.modules.sellers.models import Seller
    from app.modules.carts.models import ProductReservation
else:
    Seller = "Seller"
    ProductReservation = "ProductReservation"

products_categories_association_table = Table(
    "products_categories_association",
    Base.metadata,
    db.Column("product_id", db.ForeignKey("products.id"), primary_key=True),
    db.Column("product_category_id", db.ForeignKey("product_categories.id"), primary_key=True),
)

products_keywords_association_table = Table(
    "products_keywords_association",
    Base.metadata,
    db.Column("product_id", db.ForeignKey("products.id"), primary_key=True),
    db.Column("keyword_id", db.ForeignKey("keywords.id"), primary_key=True)
)


class ProductCategory(db.Model):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)

    products: Mapped[List[Product]] = db.relationship(
        "Product", secondary=products_categories_association_table, back_populates="categories"
    )

    def __repr__(self):
        return f"<ProductCategory name={self.name} description={self.description}>"

    def to_json(self):
        return {
            "guid": self.guid,
            "name": self.name,
        }


class Keyword(db.Model):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    key: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    reference_count: Mapped[int] = mapped_column(db.Integer, nullable=False, default=0)

    products: Mapped[List[Product]] = db.relationship(
        "Product", secondary=products_keywords_association_table, back_populates="keywords"
    )

    def __repr__(self):
        return f"<Keyword key={self.key} reference_count={self.reference_count}>"

    def to_json(self):
        return {
            "key": self.key,
            "reference_count": self.reference_count,
        }


class ProductHistory(db.Model):
    __tablename__ = "product_history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    product_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey("products.id"), nullable=False)

    sequence: Mapped[int] = mapped_column("sequence", db.Integer, nullable=False, default=0)
    price: Mapped[float] = mapped_column("price", db.Float, nullable=False)
    currency: Mapped[str] = mapped_column("currency", db.String(3), nullable=False)
    stock: Mapped[int] = mapped_column("stock", db.Integer, nullable=False)

    product = db.relationship("Product", back_populates="history")

    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    def __repr__(self):
        return (f"<ProductHistory product_id={self.product_id} sequence={self.sequence} price={self.price}"
                f"currency={self.currency} stock={self.stock}>")


class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
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

    seller: Mapped[Seller] = db.relationship("Seller", back_populates="products")
    reservations: Mapped[List[ProductReservation]] = db.relationship("ProductReservation", back_populates="product")
    categories: Mapped[List[ProductCategory]] = db.relationship(
        ProductCategory, secondary=products_categories_association_table, back_populates="products"
    )
    keywords: Mapped[List[Keyword]] = db.relationship(
        Keyword, secondary=products_keywords_association_table, back_populates="products"
    )
    history: Mapped[List[ProductHistory]] = db.relationship(
        ProductHistory, back_populates="product"
    )

    def __repr__(self):
        return (f"<Product guid={self.guid} owner_seller_id={self.owner_seller_id} name={self.name} "
                f"description={self.description} brand={self.brand} is_second_hand={self.is_second_hand} "
                f"sequence={self.sequence} price={self.price} currency={self.currency} stock={self.stock}>")

    def to_json(self):
        return {
            "guid": self.guid,
            "owner_seller_id": self.owner_seller_id,
            "name": self.name,
            "description": self.description,
            "brand": self.brand,
            "is_second_hand": self.is_second_hand,
            "sequence": self.sequence,
            "price": self.price,
            "currency": self.currency,
            "stock": self.stock,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
            "categories": [c.to_json() for c in self.categories],
            "keywords": [k.key for k in self.keywords],
        }
