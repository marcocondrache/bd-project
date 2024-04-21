from werkzeug.security import generate_password_hash

from app.modules.users.models import User
from extensions import db


def create_user(email: str, given_name: str, family_name: str, password: str):
    user = User(email=email, given_name=given_name, family_name=family_name, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


def update_user(user_id: int, password: str):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return None
    user.password = generate_password_hash(password)
    db.session.commit()
    return user
