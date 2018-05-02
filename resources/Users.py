import requests
from lib.utils import generateUUID, verify_password, generate_session_ticket, validate_ticket, db
from flask import jsonify, request
from flask_restful import Resource
from boto3.dynamodb.conditions import Key

table = db.Table('users')


class Users(Resource):


    def post(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        self.putUserData(email=email, password=password)
        return [], 204
    

    def put(self):
        json_data = request.get_json(force=True)
        email = json_data['email']
        password = json_data['password']
        ticket = json_data['ticket']
        response = table.get_item(TableName='users', Key={ 'email':email })

        pw_to_validate = response["Item"].get("password")
        authid = response["Item"].get("authid")
        active_ticket = response["Item"].get("ticket")
        ticket_expires = response["Item"].get("ticket_expires")
        is_ticket_valid = validate_ticket(ticket, active_ticket, ticket_expires)
        is_verified = verify_password(password, pw_to_validate)
        self.putUserData(email, password, authid)
        return { "email": email, "verified": is_verified, "valid_session": is_ticket_valid, "authid": authid }


    def putUserData(self, email, password, authid=generateUUID()):
        session_data  = generate_session_ticket()
        ticket = session_data.get("ticket")
        ticket_expires = session_data.get("expires")

        table.put_item(
            Item={
                    'authid': authid,
                    'email': email,
                    'password': password, 
                    'ticket': ticket,
                    'ticket_expires': ticket_expires
                }
            )


