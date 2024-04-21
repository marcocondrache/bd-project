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
