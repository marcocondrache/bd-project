from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def seller_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.sellers:
            return redirect(url_for('home.index_view'))
        return f(*args, **kwargs)

    return decorated_function
