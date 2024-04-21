from app.modules.buyers.models import Buyer
from extensions import db


def create_buyer(destination_address: str, card_number: str, user_id: int):
    buyer = Buyer(destination_address=destination_address, card_number=card_number, user_id=user_id)
    db.session.add(buyer)
    db.session.commit()
    return buyer


def update_buyer(user_id: int, destination_address: str, card_number: str):
    buyer = Buyer.query.filter_by(user_id=user_id).first()
    if not buyer:
        return None
    buyer.destination_address = destination_address
    buyer.card_number = card_number
    db.session.commit()
    return buyer
