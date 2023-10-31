from functools import wraps
import os

from flask import Blueprint, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required
from website import db

from website.models import User

def restrict_user(current_user, user_type):
    def decorator(route_function):
        @wraps(route_function)
        def decorated_function(*args, **kwargs):
            if not current_user or not current_user.__class__.__name__ in str(user_type):
                return render_template('401.html')
            return route_function(*args, **kwargs)
        return decorated_function
    return decorator
