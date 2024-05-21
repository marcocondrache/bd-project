from functools import wraps

from flask import redirect, url_for, abort
from flask_login import current_user


def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.sellers:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def buyer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.buyers:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
