from flask import Flask, Blueprint
from flask_restful import Api
from resources.Vitals import Vitals
from flask_cors import CORS


bp = Blueprint('api', __name__)
api = Api(bp)
app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/api')
CORS(app, resources={r"/api/*": { "origins": "*", "supports_credentials": True}})


# Route
api.add_resource(Vitals, '/v1/me/vitals')


if __name__ == "__main__":
    # app = create_app("config")
    app.run(debug=True)