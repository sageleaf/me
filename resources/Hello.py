import requests
from flask_restful import Resource

class Hello(Resource):
    def get(self):
      req = requests.get('https://api.humanapi.co/v1/human/medical/allergies?access_token=demo')

      return req.json()