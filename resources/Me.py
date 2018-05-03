import requests
from lib.utils import verify_password
from lib.db_utils import get_user_record, put_user_data
from constants.errors import VALVE_100, VALVE_103
from flask import abort, jsonify, request
from flask_restful import Resource
from models.User import User
from middleware.validate_user import validate_user

class Me(Resource):
    method_decorators = {'get': [validate_user]}

    def get(self):
        return { "session": "ok"  }
    

    def put(self):
        json_data = request.get_json(force=True)
        email = json_data.get("email")
        password = json_data.get("password")

        if not email or not password:
            abort(VALVE_100)

        user = User(email, password)
        existing_user = user.get_user_from_store()

        if not existing_user is None:
            is_user_valid = user.validate_password(password)
            if is_user_valid:
                updated_user = user.update_store()
                return {
                    "email": updated_user.get("email"),
                    "authid": updated_user.get("authid"),
                    "ticket": updated_user.get("ticket"),
                    "expires": updated_user.get("ticket_expires"),
                }
            else:
                abort(VALVE_103)
        else:
            user.create_new()


    




