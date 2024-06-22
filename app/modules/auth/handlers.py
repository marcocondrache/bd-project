from uuid import UUID

from werkzeug.security import check_password_hash, generate_password_hash

from app.modules.buyers.models import Buyer
from app.modules.users.models import User
from extensions import login_manager, db


@login_manager.user_loader
def load_user(user_guid: str):
    """
    Load a user by its guid. This function is used by Flask-Login.
    :param user_guid: the guid of the user
    :return: the retrieved user or None
    """
    if not UUID(user_guid):
        return None
    return User.query.filter_by(guid=UUID(user_guid)).first()


def get_user_by_email(email: str):
    """
    Get a user by its email.
    :param email: the email of the user
    :return: the retrieved user or None
    """
    return User.query.filter_by(email=email).first()


def validate_user(email: str, password: str):
    """
    Validate a user by its email and password. Return the user if the credentials are correct, None otherwise.
    :param email: the email of the user
    :param password: the password of the user
    :return: the user if the credentials are correct, None otherwise
    """
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None


def register_user(
    email: str, given_name: str, family_name: str, password: str, destination_address: str, card_number: str
):
    """
    Register a new user.
    :param email: the email of the user
    :param given_name: the given name of the user
    :param family_name: the family name of the user
    :param password: the password of the user
    :param destination_address: the destination address of the buyer
    :param card_number: the card number of the buyer
    :return: the created user
    """
    user = User(email=email, given_name=given_name, family_name=family_name, password=generate_password_hash(password))
    db.session.add(user)
    buyer = Buyer(destination_address=destination_address, card_number=card_number, user=user)
    db.session.add(buyer)
    db.session.commit()
    return user
