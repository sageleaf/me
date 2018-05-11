import os
import json
import requests
from flask_restful import Resource
from flask import request, jsonify
from app import db
from ..models.Users import Users, user_schema
from config import HUMAN_API_CLIENT_SECRET

class Me(Resource):

    def get(self):

        data = Users.query.filter_by(email=email).first()
        results = user_schema.dump(data)

        return jsonify(
            email=results.data.get("email"),
            name=results.data.get("name"),
            phone=results.data.get("phone"),
            hid_public_token=results.data.get("hid_public_token")
        )

    def post(self):
        body = request.get_json()
        email = body.get("email")
        name = body.get("name")
        phone = body.get("phone")

        if email is not None:
            user = Users.query.filter_by(email=email).first()

            if user is not None:
                user = user_schema.dump(user)
                return user
            else:
                newUser = Users(email=email, name=name, phone=phone)
                db.session.add(newUser)
                db.session.commit()


        data = Users.query.filter_by(email=email).first()
        results = user_schema.dump(data)

        return jsonify(
            email=results.data.get("email"),
            name=results.data.get("name"),
            phone=results.data.get("phone")
        )

# class Me(Resource):

#     def get(self):
#         # req = requests.post('https://user.humanapi.co/v1/connect/tokens', data=body)
#         return "ok"

#     def post(self):
#         body = request.get_json()
#         email = body.get("email")
#         name = body.get("name")
#         phone = body.get("phone")

#         if email is not None:
#             user = Users.query.filter_by(email=email).first()

#             if user is not None:
#                 user = user_schema.dump(user)
#                 return user
#             else:
#                 newUser = Users(email=email, name=name, phone=phone)
#                 db.session.add(newUser)
#                 db.session.commit()


#         data = Users.query.filter_by(email=email).first()
#         data = user_schema.dump(data)

#         return data
