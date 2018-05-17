from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from scout_apm.flask import ScoutApm
from scout_apm.flask.sqlalchemy import instrument_sqlalchemy

db = SQLAlchemy()

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    CORS(app, resources={r"/api/*": { "origins": "*", "supports_credentials": True}})
    db.init_app(app)

    ScoutApm(app)
    instrument_sqlalchemy(db)

    from .api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.config['SCOUT_NAME'] = "SAGE_LEAF_ME"

    return app