from flask import Blueprint
from flask_restful import Api
from resources.Allergies import Allergies
from resources.Me import Me

bp = Blueprint('api', __name__)
api = Api(bp)

# Route
# @auth.verify_Login
api.add_resource(Allergies, '/v1/allergies')
api.add_resource(Me, '/v1/me')