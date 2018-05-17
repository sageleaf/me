import os
import json
import requests
from flask import Blueprint
from flask_restful import Api
from .routes.Me import Me, VerifyMe


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


# Route
api.add_resource(Me, '/v1/ping')
api.add_resource(VerifyMe, '/v1/verify')



