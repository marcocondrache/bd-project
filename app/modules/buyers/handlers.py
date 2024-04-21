from app.modules.buyers.models import Buyer
from app.modules.users.models import User
from extensions import db


def create_buyer(destination_address: str, card_number: str, user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    buyer = Buyer(destination_address=destination_address, card_number=card_number, user_id=user_id)
    db.session.add(buyer)
    db.session.commit()
    return user


def update_buyer(buyer_id: int, destination_address: str, card_number: str):
    buyer = Buyer.query.filter_by(id=buyer_id).first()
    if not buyer:
        return None
    buyer.destination_address = destination_address
    buyer.card_number = card_number
    db.session.commit()
    return buyer
