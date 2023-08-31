"""
Decorators > decorators.py
Decorators for the application.
"""

# Imports
from functools import wraps
from flask import abort
from flask_login import current_user


# Decorator to check if user is an Admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in [
            "admin"
        ]:
            return abort(403)

        return f(*args, **kwargs)

    return decorated_function
