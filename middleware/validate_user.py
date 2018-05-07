import datetime
from functools import wraps
from flask import abort, jsonify, request, g
from lib.db_utils import db_update_user_field
from lib.utils import validate_ticket, extend_ticket_life
from models.User import User


def validate_user(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs): 
        authid = request.cookies.get("authid")
        email = request.cookies.get("email")
        ticket = request.cookies.get("ticket")
        if authid is None or ticket is None:
            abort(jsonify(code="VALVE-400", message="session is invalid", detail="insufficient criteria for authentication"))
        
        user = User(email, None, None, None, authid)
        is_sesssion_valid = user.validate_user_ticket(ticket)
        if not is_sesssion_valid:
            abort(jsonify(code="VALVE-400", message="session is invalid"))

        new_ticket_expiration_date = extend_ticket_life()
        db_update_user_field(key=authid, field="ticket_expires", value=new_ticket_expiration_date["expires"])
        g.user = user.get_user_from_store()
        return f(*args, **kwargs)
    return func_wrapper
