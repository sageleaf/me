# from flask import Flask
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
# from scout_apm.flask import ScoutApm
# from scout_apm.flask.sqlalchemy import instrument_sqlalchemy
# from config import SCOUT_KEY, SCOUT_LOG_LEVEL, SCOUT_MONITOR, SCOUT_NAME
# db = SQLAlchemy()

# def create_app(config_filename):
#     app = Flask(__name__)
#     app.config.from_object(config_filename)
#     CORS(app, resources={r"/api/*": { "origins": "*", "supports_credentials": True}})
#     db.init_app(app)

#     ScoutApm(app)
#     instrument_sqlalchemy(db)

#     from .api import api_blueprint
#     app.register_blueprint(api_blueprint, url_prefix='/api')
#     app.config['SCOUT_MONITOR'] = SCOUT_MONITOR
#     app.config['SCOUT_LOG_LEVEL'] = SCOUT_LOG_LEVEL
#     app.config['SCOUT_KEY'] = SCOUT_KEY
#     app.config['SCOUT_NAME'] = SCOUT_NAME

#     return app


import json
from aiohttp.web import Response, Application, json_response
import aiohttp_cors
from .lib.database import db_init
from .lib.utils import get_config, get_file


def create_app():
    file_name = get_file(path="config", extention="py")
    config = get_config(file_name=file_name)
    app = Application()
    app["config"] = config
    db_init(app)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
        })

    from .api.routes import handle_authenticate_profile, handle_token_validation, handle_token_exchange
    cors.add(app.router.add_post('/api/v1/profile', handle_authenticate_profile))
    cors.add(app.router.add_get('/api/v1/exchange', handle_token_exchange))
    cors.add(app.router.add_get('/api/v1/validation', handle_token_validation))

    return app 