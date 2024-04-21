from extensions import login_manager, db
from app.modules.users.models import User
from werkzeug.security import generate_password_hash, check_password_hash

from uuid import UUID


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

def create_user(email: str, given_name: str, family_name: str, password: str):
    user = User(email=email, given_name=given_name, family_name=family_name, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user
