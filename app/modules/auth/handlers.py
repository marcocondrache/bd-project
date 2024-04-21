from uuid import UUID

from werkzeug.security import check_password_hash

from app.modules.buyers.handlers import create_buyer
from app.modules.users.handlers import create_user
from app.modules.users.models import User
from extensions import login_manager


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
    user = create_user(email, given_name, family_name, password)
    create_buyer(destination_address, card_number, user.id)
    return user
