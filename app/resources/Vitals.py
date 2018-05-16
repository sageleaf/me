import os
import json
import uuid
import requests
from flask_restful import Resource
from flask import request, jsonify
from datetime import datetime
from ..models.Vitals import Vitals as VitalsModel, vitals_schema
from ..models.Profile import Profile, profile_schema


class Vitals(Resource):
    # method_decorators = {'get': [validate_user]}

    def get(self):
        # TODO: validae the user
        data_key = request.args.get("filter")
        profile_id = request.cookies.get('profile_id')
        query = VitalsModel.query
        vitals = []
        if data_key is not None:
            query = query.filter_by(profile_id=profile_id, data_key=data_key)
        else :
            query = query.filter_by(profile_id=profile_id) 

        items = query.all()
        if type(items) == list:
            for item in items:
                vital_dump = vitals_schema.dump(item)
                # TODO: check for error -> if vital_dump.error:
                vitals.append(vital_dump.data)

        return vitals


    def post(self):
        # TODO: validae the user
        body = request.get_json()
        if type(body) == list:
            entries = []
            profile_id = request.cookies.get('profile_id')
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for entry in body:
                manual_data_id = str(uuid.uuid4())  
                data_key = entry.get("data_key")
                data_value = entry.get("data_value")
                performed_at = entry.get("performed_at")
                # @data_key: one_of("keytones", "glucose", ) 
                newEntry = VitalsModel(manual_data_id=manual_data_id, profile_id=profile_id, created_at=created_at, data_key=data_key, data_value=data_value, performed_at=performed_at)
                newEntry.commit()
                vital = VitalsModel.query.filter_by(manual_data_id=manual_data_id).first()
                vital_dump = vitals_schema.dump(vital)
                # TODO: check for error -> if vital_dump.error:
                entries.append(vital_dump.data)

            return entries

        else :
            return { "code": "VALVE-400", "message":"post body is malformed, must be a list" }, 400
