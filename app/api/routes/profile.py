import asyncio
from aiohttp.web import json_response
from sqlalchemy import Column, Integer, String, DateTime
from marshmallow import Schema, fields
from ...lib.database import Base, session
from ...lib.tokens import encode_jwt_token, decode_jwt_token
from ...lib.email import send_email
from ...lib.loggers import logger
from ...constants.errors import generate_error
from ...lib.utils import (
    generate_uuid,
    get_now,
    generate_verification_code,
    get_future_date,
    is_date_passed,
    parse_auth_header
)


# route handlers
async def handle_authenticate_profile(request) -> json_response:
    post_body = await request.json()
    (profile_id, email), error = maybe_add_profile(post_body)

    if error:
        return json_response(generate_error('data_persistance', detail=error), status=500)

    session_id, verification_code = generate_session(profile_id=profile_id)
    asyncio.ensure_future(generate_verification_email(email=email, verification_code=verification_code))

    return json_response({"session_id": session_id})


async def handle_get_profile(request) -> json_response:
    profile_id = request.headers.get("profile_id", None)

    if profile_id is None:
        return json_response(generate_error('need_more_info', detail="invalid profile"), status=400)

    profile = Profile.query.filter_by(profile_id=profile_id).first()
    data, error = ProfileSchema().dump(profile)

    if error or profile is None:
        return json_response(generate_error('data_retrieval', detail=error), status=500)

    return json_response({
        "email": data.get("email"),
        "name": data.get("first_name"),
        "phone": data.get("phone_number"),
        "confirmed_at": data.get("confirmed_at")
    })


async def handle_token_exchange(request) -> json_response:
    # validate a users session
    # in: (query string)
    #   code -> verification_code: sent via email, SMS
    #   session -> session_id, sent from POST `/api/me``
    # out: 
    #   token
    #
    query = request.rel_url.query
    verification_code = query["code"]
    session_id = query["session"]

    if verification_code is None or session_id is None:
        return json_response(generate_error('invalid_session', detail=None), status=400)

    session = Session.query.filter_by(session_id=session_id).first()
    session_dump = SessionSchema().dump(session)
    session_data = session_dump.data

    if session_data.get("status") == 1:
        return json_response(generate_error('jwt_error', detail= "session already validated"), status=400)

    if is_date_passed(session_data.get("expires")):
        return json_response(generate_error('invalid_session', detail="session is not valid"), status=400)

    session.status = 1
    session.modify()
    
    profile_id = session_data.get("profile_id")
    auth_token, encode_error = encode_jwt_token(profile_id)

    if encode_error:
        return json_response(generate_error('catastrophic', detail=None), status=500)

    readable_auth_token = auth_token.decode()

    response = json_response({"token": readable_auth_token }, status=200)

    response.set_cookie("token", readable_auth_token, secure=True)

    asyncio.ensure_future(confirm_profile_validation(profile_id=profile_id))

    return response


async def handle_token_validation(request) -> json_response:
    # ping server to validate user 
    # in: (cookie, auth header)
    #   token -> passed via cooke
    #   jwt -> passed via auth header
    # out: 
    #   status -> `ok` or `not ok`
    auth = parse_auth_header(auth_type='jwt', auth_header=request.headers.get("Authorization"))
    token = request.cookies.get("token") or auth or None

    if token is not None:
        valid_token, token_error = decode_jwt_token(token)
        if token_error:
            return json_response(generate_error('catastrophic', detail=None), status=500)
        else :
            return json_response({ "status": "ok"})
    else:
        return json_response(generate_error('need_more_info', detail="missing token"), status=401)


# helpers
def maybe_add_profile(post_body) -> (list, str):
    email = post_body.get("email")
    phone_number = post_body.get("phone")
    first_name = post_body.get("first_name")

    if email is None:
        return None, { "error": "need more data, aka an email address" }

    profile = Profile.query.filter_by(email=email).first()
    data, error = ProfileSchema().dump(profile)

    if error:
        return None, { "error": "internal db issue" }
        return json_response(generate_error('data_retrieval', detail=error), status=500)

    profile_id = data.get("profile_id")

    if profile_id is not None:
        # already esitst
        return (profile_id, email), None
    
    if first_name is None is None or phone_number is None:
        return json_response(generate_error('need_more_info', detail="need more data to create a profile"), status=401)
    else :
        profile_id = generate_new_profile(email=email, first_name=first_name, phone_number=phone_number)

    return (profile_id, email), None


def generate_session(profile_id) -> (str, str):
    # TODO: validate profile data worked `newProfile.query.filter_by(profile_id=profile_id)`
    session_id = generate_uuid()
    verification_code = generate_verification_code()
    newSession = Session(profile_id=profile_id, session_id=session_id, verification_code=verification_code, expires=get_future_date(90))
    newSession.commit()
    logger.info("new session generated for profile_id " + profile_id)
    return (session_id, verification_code)


async def confirm_profile_validation(profile_id) -> None:
    profile = Profile.query.filter_by(profile_id=profile_id).first()
    data, error = ProfileSchema().dump(profile)
    profile.confirmed_at = get_now()
    profile.modify()
    logger.info("profile confrimed for profile_id " + profile_id)


def generate_new_profile(email, first_name, phone_number) -> str:
    profile_id = generate_uuid()
    newProfile = Profile(profile_id=profile_id, created_at=get_now(), email=email, first_name=first_name, phone_number=phone_number)
    newProfile.commit()
    logger.info("new profile generated for profile_id " + profile_id)
    return profile_id


async def generate_verification_email(email, verification_code) -> None:
    try:
        msg = "Verify using this code: " + str(verification_code)
        logger.info("email generated for " + email)
        send_email(email=email, subject="Verify Your Account", message=msg)
    except Exception:
        logger.error("error generating email: " + Exception)


# database schemas
class Profile(Base):
    __tablename__ = 'user_profiles'
    profile_id = Column(String(50), primary_key=True)
    created_at = Column(DateTime)
    email = Column(String(50))
    phone_number = Column(String(10))
    first_name = Column(String(50))
    confirmed_at = Column(DateTime)

    def __init__(self, profile_id, created_at, email, first_name, phone_number):
        self.profile_id = profile_id
        self.created_at = created_at
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.confirmed_at = None

    def commit(self):
        session.add(self)
        session.commit()

    def modify(self):
        session.merge(self)
        session.commit()


class ProfileSchema(Schema):
    __tablename__ = 'profile'
    profile_id = fields.Str()
    created_at = fields.Str()
    email = fields.Str()
    phone_number = fields.Str()
    first_name = fields.Str()
    confirmed_at = fields.Str()


class Session(Base):
    __tablename__ = 'session'
    session_id = Column(String(100), primary_key=True)
    profile_id = Column(String(100))
    verification_code = Column(String(100))
    expires = Column(DateTime)
    status = Column(String(100))

    def __init__(self, profile_id, session_id, verification_code, expires):
        self.session_id = session_id
        self.profile_id = profile_id
        self.verification_code = verification_code
        self.expires = expires
        self.status = 0
    
    def commit(self):
        session.add(self)
        session.commit()
    
    def modify(self):
        session.merge(self)
        session.commit()


class SessionSchema(Schema):
    __tablename__ = 'session'
    profile_id = fields.Str()
    session_id = fields.Str()
    verification_code = fields.Str()
    expires = fields.DateTime()
    status = fields.Str()