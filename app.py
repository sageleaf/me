from flask import Flask, Blueprint
from flask_restful import Api
from resources.Vitals import Vitals
# from resources.Me import Me
# from resources.Connections import Connections
from flask_cors import CORS

bp = Blueprint('api', __name__)
api = Api(bp)

# Route
# @auth.verify_Login
api.add_resource(Vitals, '/v1/me/vitals')


def create_app(config_filename):
    app = Flask(__name__)
    # app.config.from_object(config_filename)
    # from app import bp
    app.register_blueprint(bp, url_prefix='/api')

    CORS(app, resources={r"/api/*": { "origins": "*", "supports_credentials": True}})

    return app


if __name__ == "__main__":
    app = create_app("config")
    app.run(debug=True)