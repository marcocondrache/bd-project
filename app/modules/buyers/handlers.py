from app.modules.buyers.models import Buyer
from extensions import db


def update_buyer(user_id: int, destination_address: str, card_number: str):
    """
    Update the destination address and card number of a buyer.
    Return the updated buyer if successful, None otherwise.
    :param user_id: the user id
    :param destination_address: the updated destination address of the buyer
    :param card_number: the updated card number of the buyer
    :return the updated buyer
    """
    buyer = Buyer.query.filter_by(user_id=user_id).first()
    if not buyer:
        return None
    buyer.destination_address = destination_address
    buyer.card_number = card_number
    db.session.commit()
    return buyer
