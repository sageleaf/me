import os
import json
import uuid
import requests
from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from ..models.Nutrition import Nutrition as NutritionModel, nutrition_schema
from ..models.Users import Users, user_schema
from config import NUTRITIONIX_BASE_URL, NUTRITIONIX_PATH_NUTRIENTS, NUTRITIONIX_PATH_SEARCH, NUTRITIONIX_APP_ID, NUTRITIONIX_APP_KEY


class Search(Resource):
    def get(self):
        query = request.args.get("query")
        if query is None: 
            return {
                "error": "VALVE-400",
                "message": "we need to search for something... make sure you add a the query param `query`"
            }

        params = { "query": query }
        headers= {
            "x-app-id": NUTRITIONIX_APP_ID,
            "x-app-key": NUTRITIONIX_APP_KEY
        }
        req = requests.get(NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_SEARCH, params=params, headers=headers)

        return req.json()


class Nutrition(Resource):
    def get(self):
        query = request.args.get("query")
        if query is None: 
            return {
                "error": "VALVE-400",
                "message": "we need to search for something... make sure you add a the query param `query`"
            }

        pay_load = { "query": query }
        headers= {
            "x-app-id": NUTRITIONIX_APP_ID,
            "x-app-key": NUTRITIONIX_APP_KEY
        }
        print( "HEADERS::::", headers )
        req = requests.post(NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_NUTRIENTS, data=pay_load, headers=headers)

        return req.json()
