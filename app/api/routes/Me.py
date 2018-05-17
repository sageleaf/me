import json
import requests
from flask_restful import Resource
from flask import request, jsonify, make_response
from app import db
from ...models.Profile import Profile, profile_schema
from ...models.Session import Session, session_schema
from ...lib.tokens import encode_jwt_token, decode_jwt_token
from ...lib.email import send_email
from ...lib.utils import generate_uuid, get_now, generate_verification_code, get_future_date, is_date_passed


def generate_session(profile_id):
    # TODO: validate profile data worked `newProfile.query.filter_by(profile_id=profile_id)`
        session_id = generate_uuid()
        verification_code = generate_verification_code()
        newSession = Session(profile_id=profile_id, session_id=session_id, verification_code=verification_code, expires=get_future_date(90))
        newSession.commit()
        return (session_id, verification_code)


def generate_new_profile(email, first_name, last_name, phone_number):
        profile_id = generate_uuid()
        newProfile = Profile(profile_id=profile_id, created_at=get_now(), email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
        newProfile.commit()
        return profile_id


def generate_verification_email(email, verification_code):
        msg = "Verify using this code: " + str(verification_code)
        send_email(email=email, subject="Verify Your Account", message=msg)


def parse_auth_header(auth_type, auth_header=""):
    auth = auth_header.split()
    if len(auth) == 2 and auth[0] == auth_type:
        return auth[1]
    else:
        return None


class Ping(Resource):
    # validate a users session
    def get(self): 
        # ping server to validate user 
        # in: (cookie, auth header)
        #   token -> passed via cooke
        #   jwt -> passed via auth header
        # out: 
        #   status -> `ok` or `not ok`
        auth = parse_auth_header(auth_type='jwt', auth_header=request.headers.get("Authorization"))
        token = request.cookies.get("token") or auth or None

        if token is not None:
            valid_token = decode_jwt_token(token)
            return { "status": "ok"}, 200
        else:
            return { "status": "not ok" }, 401


class Exchange(Resource):
    # validate a users session
    # in: (query string)
    #   code -> verification_code: sent via email, SMS
    #   session -> session_id, sent from POST `/api/me``
    # out: 
    #   token
    #
    def get(self): 
        verification_code = request.args.get('code')
        session_id = request.args.get('session')

        if verification_code is None or session_id is None:
            return { "status": "invalid session" }, 400

        session = Session.query.filter_by(session_id=session_id).first()
        session_dump = session_schema.dump(session)
        session_data = session_dump.data

        if session_data.get("status") == 1:
            return { "status": "session already validated" }, 400

        if is_date_passed(session_data.get("expires")):
            return { "status": "session is not valid" }, 400

        session.status = 1
        session.modify()
        
        auth_token= encode_jwt_token(session_data.get("profile_id"))
        readable_auth_token = auth_token.decode()

        response = make_response(jsonify(
            token=readable_auth_token
        ), 200)

        response.set_cookie("token", readable_auth_token, secure=True)

        return response



class Profile(Resource):
    def post(self): 
        # create a new profile
        # in: (post body)
        #   email -> verification_code: sent via email, SMS
        #   phone -> session_id, sent from POST `/api/me``
        #   first_name -> session_id, sent from POST `/api/me``
        #   last_name -> session_id, sent from POST `/api/me``
        # out: 
        #   session_id
        # trigger: (email or SMS)
        #   verification_code
        #
        post_body = request.get_json(force=True)
        email = post_body.get("email")
        phone_number = post_body.get("phone")
        first_name = post_body.get("first_name")
        last_name = post_body.get("last_name")

        # legit can't do anything, we need at minimum an email
        if email is None:
            return { "error": "need more data, aka an email address" }, 400

        # look for an existing user. 
        user = Profile.query.filter_by(email=email).first()
        user_dump = profile_schema.dump(user) 
        user_data = user_dump.data
        profile_id = user_data.get("profile_id")

        if profile_id is None:
            #we have a user. 
            if first_name is None or last_name is None or phone_number is None:
                return { "error": "need more data" }, 400
            else: 
                profile_id = generate_new_profile(email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)


        session_id, verification_code = generate_session(profile_id=profile_id)
        generate_verification_email(email=email, verification_code=verification_code)

        return {
            "session_id": session_id
        }

