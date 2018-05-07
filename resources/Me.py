import requests
from constants.errors import VALVE_100, VALVE_103
from flask import abort, jsonify, request, make_response, g
from flask_restful import Resource
from models.User import User
from middleware.validate_user import validate_user

class Me(Resource):
    method_decorators = {'get': [validate_user]}

    def get(self):
        user = g.user
        email = user.get("email")
        authid = user.get("authid")
        ticket = user.get("ticket")
        expires = user.get("ticket_expires")
        response = make_response(jsonify( session="ok", email=email, authid=authid, ticket=ticket), 200)
        return response


    def post(self):
        json_data = request.get_json(force=True)
        email = json_data.get("email")
        password = json_data.get("password")
        name = json_data.get("name")
        phone = json_data.get("phone")

        if email is None or password is None or name is None or phone is None:
            VALVE_100, 401
        
        user = User(email, password, name, phone, None)
        existing_user = user.search_for_user_by("email", email)
        if not len(existing_user):
            # Create a New User
            updated_user = user.create_new_user()
            authid=updated_user["authid"]
            ticket=updated_user["ticket"]
            create_date=updated_user["create_date"]
            response = make_response(jsonify(
                session="ok",
                authid=authid,
                email=email,
                name=name,
                phone=phone,
                ticket=ticket,
                create_date=create_date
            ), 200)

            response.set_cookie("email", email, domain=".hyh.com", path="/", secure=True)
            response.set_cookie("authid", authid, domain=".hyh.com",path="/", secure=True)
            response.set_cookie("ticket", ticket, domain=".hyh.com",path="/", secure=True)

            return response
        
        else:
            return {
                "code" : "VALVE_102",
                "message": "user alraedy exists",
                "detail": "TODO -> don't send this info, easier to hack"
            }, 400


    # def put(self):
    #     json_data = request.get_json(force=True)
    #     email = json_data.get("email")
    #     password = json_data.get("password")

    #     if not email or not password:
    #         VALVE_100, 401
        
    #     user = User(email, password)
    #     existing_user = user.get_user_from_store()

    #     if not existing_user is None:
    #         is_user_valid = user.validate_password(password)
    #         if is_user_valid:
    #             updated_user = user.update_store()
    #             email = updated_user.get("email")
    #             authid = updated_user.get("authid")
    #             ticket = updated_user.get("ticket")

    #             response = make_response(jsonify(
    #                 session="ok",
    #                 email=email,
    #                 authid=authid,
    #                 ticket=ticket
    #             ), 200)

    #             response.set_cookie("email", email, domain=".hyh.com", path="/", secure=True)
    #             response.set_cookie("authid", authid, domain=".hyh.com",path="/", secure=True)
    #             response.set_cookie("ticket", ticket, domain=".hyh.com",path="/", secure=True)

    #             return response                
    #         else:
    #             return VALVE_103, 401
    #     else:
    #         return VALVE_103, 401







    




