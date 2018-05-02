from flask import Flask

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    from app import bp
    app.register_blueprint(bp, url_prefix='/api')
    return app


if __name__ == "__main__":
    application = create_app("config")
    application.run(debug=True)