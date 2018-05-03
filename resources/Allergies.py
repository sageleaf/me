import requests
from flask_restful import Resource
from middleware.validate_user import validate_user


class Allergies(Resource):
    decorators = [validate_user]

    def get(self, *args, **kwargs):
      req = requests.get('https://api.humanapi.co/v1/human/medical/allergies?access_token=demo')
      return req.json()