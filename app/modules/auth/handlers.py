from uuid import UUID

from flask_login import current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.buyers.models import Buyer
from app.modules.users.models import User
from extensions import login_manager, db


@login_manager.user_loader
def load_user(user_guid: str):
    if not UUID(user_guid):
        return None
    return User.query.filter_by(guid=UUID(user_guid)).first()


def get_user_by_email(email: str):
    return User.query.filter_by(email=email).first()


# Login user
def validate_user(email: str, password: str):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def register_user(
    email: str, given_name: str, family_name: str, password: str, destination_address: str, card_number: str
):
    user = User(email=email, given_name=given_name, family_name=family_name, password=generate_password_hash(password))
    db.session.add(user)
    buyer = Buyer(destination_address=destination_address, card_number=card_number, user_id=user.id)
    db.session.add(buyer)
    db.session.commit()
    return user


def is_seller():
    return bool(current_user.sellers)
