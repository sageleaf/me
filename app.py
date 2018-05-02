from flask import Blueprint
from flask_restful import Api
from resources.Allergies import Allergies
from resources.Users import Users
from resources.Me import Login

bp = Blueprint('api', __name__)
api = Api(bp)

# Route
api.add_resource(Allergies, '/v1/allergies')
api.add_resource(Users, '/v1/me/new')
api.add_resource(Login, '/v1/me/login')