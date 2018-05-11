import os
import json
import requests
from flask_restful import Resource
from flask import request, jsonify
from ..middleware.validate_user import requires_auth


class Validate(Resource):
    method_decorators = {'get': [requires_auth]}

    def get(self):
        return "ok"

