import requests
from flask_restful import Resource
# from middleware.validate_user import validate_user
from models.Heart import Heart
import json
import os

class Vitals(Resource):
    # decorators = [validate_user]

    def post(self):
      normalized_heart_rates = []
      req = requests.get('https://api.humanapi.co/v1/human/heart_rate/readings?access_token=demo')
      heart_rates = req.json()

      if heart_rates and len(heart_rates):
        for hr in heart_rates:
          normalized_heart_rates.append({
              "rate": hr.get("value"),
              "unit": hr.get("unit"),
              "source": hr.get("source"),
              "date": hr.get("timestamp")
          })
      return normalized_heart_rates

    def get(self):
      return os.environ.get("DB_CONNECTION")



#       import requests
# from lib.utils import verify_password
# from flask import abort, jsonify, request
# from flask_restful import Resource
# from middleware.validate_user import validate_user
# from config import HUMAN_API_CLIENT_SECRET

# class Connections(Resource):
#     # method_decorators = {'get': [validate_user]}

#     def post(self):
#         json_data = request.get_json(force=True)
#         json_data["clientSecret"] = HUMAN_API_CLIENT_SECRET

#         print( 'json_data:::', json_data )
#         req = requests.post('https://user.humanapi.co/v1/connect/tokens', data=json_data)

#         return req.json()