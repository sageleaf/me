import requests
from lib.utils import verify_password
from lib.db_utils import get_user_record, put_user_data
from constants.errors import VALVE_100, VALVE_103
from flask import jsonify, request
from flask_restful import Resource
from boto3.dynamodb.conditions import Key

class Login(Resource):

    def put(self):
        json_data = request.get_json(force=True)

        email = json_data.get("email")
        password = json_data.get("password")
        # ticket = request.cookies.get('ticket')

        if password and email:
            [error, user_login_data] = login_user(email, password)

            if not error:
                return {
                    "authid": user_login_data.get("authid"),
                    "ticket": user_login_data.get("ticket"),
                    "expires": user_login_data.get("ticket_expires"),
                }
            else:
                return error, 400

        else:
            return VALVE_100, 400


def login_user(email, password):
    user = get_user_record(email=email)

    if not user == None:
        authid         = user.get("authid")
        pw_to_validate = user.get("password")
        is_pw_verified = verify_password(password, pw_to_validate)

        if is_pw_verified:
            updated_user = put_user_data(email, password, authid)
            return [ None, updated_user ]
        else:
            return [ VALVE_103 , None ]
    else:
        new_user = put_user_data(email, password)
        return new_user
    




