import os
import json
import requests
from flask_restful import Resource
from flask import request, jsonify
from app import db
from ..models.Profile import Profile, profile_schema
from config import HUMAN_API_CLIENT_SECRET


class Callback(Resource):

    def get(self):
        body = request.get_json()
        body["clientSecret"] = HUMAN_API_CLIENT_SECRET
        req = requests.post('https://user.humanapi.co/v1/connect/tokens', data=body)

        return req.json()

