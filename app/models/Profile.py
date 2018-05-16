import uuid
import datetime
from app import db
from marshmallow import Schema, fields


class Profile(db.Model):
    __tablename__ = 'profile'
    profile_id = db.Column(db.VARCHAR(100), primary_key=True)
    created_at = db.Column(db.DATETIME)
    email = db.Column(db.VARCHAR(100))
    phone_number = db.Column(db.VARCHAR(100))
    first_name = db.Column(db.VARCHAR(100))
    last_name = db.Column(db.VARCHAR(100))

    def __init__(self, profile_id, created_at, email, first_name, last_name, phone_number):
        self.profile_id = profile_id
        self.created_at = created_at
        self.email = email
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name

    def commit(self):
        db.session.add(self)
        db.session.commit()


class ProfileSchema(Schema):
    __tablename__ = 'profile'
    profile_id = fields.Str()
    created_at = fields.Str()
    email = fields.Str()
    phone_number = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()


profile_schema = ProfileSchema()