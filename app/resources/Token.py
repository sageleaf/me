import os
import json
import requests
from flask_restful import Resource
from flask import request, jsonify
from app import db
from ..models.Users import Users, user_schema
from config import HUMAN_API_CLIENT_SECRET, HUMAN_API_BASE_URL, HUMAN_API_PATH_TOKEN


class Token(Resource):

    def post(self):
        body = request.get_json()
        body["clientSecret"] = HUMAN_API_CLIENT_SECRET
        req = requests.post(HUMAN_API_BASE_URL + HUMAN_API_PATH_TOKEN, data=body)

        return req.json()

