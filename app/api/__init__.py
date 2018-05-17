import os
import json
import requests
from flask import Blueprint
from flask_restful import Api
from .routes.Me import Ping, Profile, Exchange


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# Route
api.add_resource(Profile, '/v1/profile')
api.add_resource(Exchange, '/v1/exchange')
api.add_resource(Ping, '/v1/ping')



