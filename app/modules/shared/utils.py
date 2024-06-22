from functools import wraps

from flask import abort
from flask_login import current_user


def seller_required(f):
    """
    Decorator to require a seller.
    :param f: the function to decorate
    :return: the decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.sellers:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function


def buyer_required(f):
    """
    Decorator to require a buyer.
    :param f: the function to decorate
    :return: the decorated function
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.buyers:
            abort(403)
        return f(*args, **kwargs)

    return decorated_function
