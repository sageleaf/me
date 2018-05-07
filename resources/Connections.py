import requests
from lib.utils import verify_password
from flask import abort, jsonify, request
from flask_restful import Resource
from middleware.validate_user import validate_user
from config import HUMAN_API_CLIENT_SECRET

class Connections(Resource):
    # method_decorators = {'get': [validate_user]}

    def post(self):
        json_data = request.get_json(force=True)
        json_data["clientSecret"] = HUMAN_API_CLIENT_SECRET

        print( 'json_data:::', json_data )
        req = requests.post('https://user.humanapi.co/v1/connect/tokens', data=json_data)

        return req.json()
    


    




