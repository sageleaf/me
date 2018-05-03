import datetime
from functools import wraps
from flask import abort, jsonify, request
from lib.db_utils import get_user_record, put_user_data
from lib.utils import validate_ticket
from models.User import User


def validate_user(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs): 
        email = request.cookies.get("email")
        ticket = request.cookies.get("ticket")
        if email is None or ticket is None:
            abort(jsonify(code="VALVE-400", message="session is invalid"))
        user = User(email)
        is_sesssion_valid = user.validate_ticket(ticket)
        if not is_sesssion_valid:
            abort(jsonify(code="VALVE-400", message="session is invalid"))
        return f(*args, **kwargs)
    return func_wrapper
