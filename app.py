from flask import Blueprint
from flask_restful import Api
from resources.Vitals import Vitals
from resources.Me import Me
from resources.Connections import Connections

bp = Blueprint('api', __name__)
api = Api(bp)

# Route
# @auth.verify_Login
api.add_resource(Vitals, '/v1/me/vitals')