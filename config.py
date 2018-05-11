from os import path, environ as env

basedir = path.abspath(path.dirname(__file__))
HUMAN_API_BASE_URL='https://user.humanapi.co/v1'
HUMAN_API_PATH_TOKEN='/connect/tokens'
HUMAN_API_CLIENT_ID=env.get("HUMAN_API_CLIENT_ID")
HUMAN_API_CLIENT_SECRET=env.get("HUMAN_API_CLIENT_SECRET")
HUMAN_API_CLIENT_APP_KEY=env.get("HUMAN_API_CLIENT_APP_KEY")
AUTH0_SECRET=env.get("DATABASE_URI")
SQLALCHEMY_DATABASE_URI=env.get("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = False
DEBUG = True
TESTING = True
NUTRITIONIX_APP_ID = env.get("NUTRITIONIX_APP_ID")
NUTRITIONIX_APP_KEY = env.get("NUTRITIONIX_APP_KEY")
NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/v2"
NUTRITIONIX_PATH_NUTRIENTS = "/natural/nutrients"
NUTRITIONIX_PATH_SEARCH = "/search/instant"




