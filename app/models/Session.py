from app import db
from marshmallow import Schema, fields


class Session(db.Model):
    __tablename__ = 'session'
    session_id = db.Column(db.VARCHAR(100), primary_key=True)
    profile_id = db.Column(db.VARCHAR(100))
    verification_code = db.Column(db.VARCHAR(100))
    expires = db.Column(db.DATETIME)
    status = db.Column(db.VARCHAR(100))

    # @status:
    # 0: unverified
    # 1: verified
    # 2: expired
    def __init__(self, profile_id, session_id, verification_code, expires):
        self.session_id = session_id
        self.profile_id = profile_id
        self.verification_code = verification_code
        self.expires = expires
        self.status = 0
    
    def commit(self):
        db.session.add(self)
        db.session.commit()
    
    def modify(self):
        db.session.merge(self)
        db.session.commit()


class SessionSchema(Schema):
    __tablename__ = 'session'
    profile_id = fields.Str()
    session_id = fields.Str()
    verification_code = fields.Str()
    expires = fields.DateTime()
    status = fields.Str()

session_schema = SessionSchema()