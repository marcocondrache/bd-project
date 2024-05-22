import uuid
from typing import List, TYPE_CHECKING

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from extensions import db
if TYPE_CHECKING:
    from app.modules.sellers.models import Seller
    from app.modules.buyers.models import Buyer
else:
    Buyer = "Buyer"
    Seller = "Seller"


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False, index=True)
    guid: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    given_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    family_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)
    created_at: Mapped[str] = mapped_column(db.DateTime, nullable=False, server_default=db.func.now())
    updated_at: Mapped[str] = mapped_column(
        db.DateTime, nullable=False, server_default=db.func.now(), onupdate=db.func.now()
    )
    deleted_at: Mapped[str] = mapped_column(db.DateTime, nullable=True)

    buyers: Mapped[List[Buyer]] = db.relationship("Buyer", back_populates="user")
    sellers: Mapped[List[Seller]] = db.relationship("Seller", back_populates="user")

    def get_id(self):
        return str(self.guid)

    def __repr__(self):
        return f"<User guid={self.guid} email={self.email} given_name={self.given_name} family_name={self.family_name}>"
