from werkzeug.security import generate_password_hash

from app.modules.users.models import User
from extensions import db


def create_user(email: str, given_name: str, family_name: str, password: str):
    """
    Create a new user. The password is hashed before storing it.
    :param email: the email of the user
    :param given_name: the given name of the user
    :param family_name: the family name of the user
    :param password: the password of the user
    :return: the created user
    """
    user = User(email=email, given_name=given_name, family_name=family_name, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


def update_user(guid: str, password: str):
    """
    Update the password of a user. The password is hashed before storing it.
    :param guid: the guid of the user
    :param password: the new password
    :return: the updated user
   """
    user = User.query.filter_by(guid=guid).first()
    if not user:
        return None
    user.password = generate_password_hash(password)
    db.session.commit()
    return user
