from app.modules.sellers.models import Seller
from extensions import db


def create_seller(user_id: int, iban: str, show_soldout_products: bool):
    """
    Create a seller. If the seller already exists, return None.
    :param user_id: the id of the user
    :param iban: the iban of the seller
    :param show_soldout_products: whether to show sold out products
    :return: the seller or None if it already exists
    """
    seller = Seller(iban=iban, show_soldout_products=show_soldout_products, user_id=user_id)
    db.session.add(seller)
    db.session.commit()
    return seller


def update_seller(user_id: int, iban: str, show_soldout_products: bool):
    """
    Update a seller. If the seller doesn't exist, return None.
    :param user_id: the id of the user
    :param iban: the iban of the seller
    :param show_soldout_products: whether to show sold out products
    :return: the seller or None if it doesn't exist
    """
    seller = Seller.query.filter_by(user_id=user_id).first()
    if not seller:
        return None
    seller.iban = iban
    seller.show_soldout_products = show_soldout_products
    db.session.commit()
    return seller
