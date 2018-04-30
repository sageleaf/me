from flask import Flask

def create_app(config_filename):
    application = Flask(__name__)
    application.config.from_object(config_filename)
    
    from app import bp
    application.register_blueprint(bp, url_prefix='/api')

    # from Model import db
    # db.init_app(app)

    return application


if __name__ == "__main__":
    application = create_app("config")
    application.run(host='0.0.0.0', debug=True)