import requests
from flask_restful import Resource
from middleware.validate_user import validate_user
from models.Heart import Heart
import json

class Vitals(Resource):
    # decorators = [validate_user]

    def get(self):
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