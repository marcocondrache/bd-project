from app.modules.sellers.models import Seller
from app.modules.users.models import User
from extensions import db


def create_seller(user_id: int, iban: str, show_soldout_products: bool):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    seller = Seller(iban=iban, show_soldout_products=show_soldout_products, user_id=user_id)
    db.session.add(seller)
    db.session.commit()
    return user


def update_seller(guid: str, iban: str, show_soldout_products: bool):
    seller = Seller.query.filter_by(guid=guid).first()
    if not seller:
        return None
    seller.iban = iban
    seller.show_soldout_products = show_soldout_products
    db.session.commit()
    return seller
