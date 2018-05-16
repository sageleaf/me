import os
import json
import requests
from flask import Blueprint
from flask_restful import Api
from ..resources.Vitals import Vitals
from ..resources.Token import Token
from .routes.Me import Me, VerifyMe
from ..resources.Callback import Callback
from ..resources.Validate import Validate
from ..resources.Nutrition import Search, Nutrition


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# Route
api.add_resource(Me, '/v1/me')
api.add_resource(VerifyMe, '/v1/me/verify')

api.add_resource(Vitals, '/v1/me/vitals')
api.add_resource(Search, '/v1/me/nutrition/search')
api.add_resource(Nutrition, '/v1/me/nutrition')

api.add_resource(Token, '/v1/connect')
api.add_resource(Callback, '/v1/callback')
api.add_resource(Validate, '/v1/validate')


