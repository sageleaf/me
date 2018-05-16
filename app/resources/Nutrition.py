import os
import json
import uuid
import requests
from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from functools import reduce
from ..models.Nutrition import Nutrition as NutritionModel, nutrition_schema
from ..models.Profile import Profile, profile_schema
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
        auth = request.headers.get('Authorization')

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
        req = requests.post(NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_NUTRIENTS, data=pay_load, headers=headers)
        body = req.json()

        resp = list(map(lambda food: {
            "name": food.get("food_name"),
            "servings": food.get("serving_qty"),
            "calories": food.get("nf_calories"),
            "fat": food.get("nf_total_fat"),
            "saturated_fat": food.get("nf_saturated_fat"),
            "cholesterol": food.get("nf_cholesterol"),
            "sodium": food.get("nf_sodium"),
            "sugars": food.get("nf_sugars"),
            "protein": food.get("nf_protein"),
            "potassium": food.get("nf_potassium"),
            "carbohydrates": food.get("nf_total_carbohydrate"),
        },body.get('foods')))

        totals = reduce(sum_dict, resp)
        return jsonify(totals=totals, foods=resp)


def sum_dict(d1, d2):
    current = dict(d1)
    for key, value in current.items():
        if key == 'name' or key == 'servings':
            current[key] = None
        else :
            current[key] = value + d2.get(key, 0)
    return current
