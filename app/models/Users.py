from app import db
from marshmallow import Schema, fields


class Users(db.Model):
    __tablename__ = 'users'
    email = db.Column(db.VARCHAR(100), primary_key=True)
    name = db.Column(db.VARCHAR(100))
    phone = db.Column(db.VARCHAR(100))
    human_id = db.Column(db.VARCHAR(100))
    hid_public_token = db.Column(db.VARCHAR(100))
    hid_access_token = db.Column(db.VARCHAR(100))

    def __init__(self, email, name, phone):
        self.email = email
        self.name = name
        self.phone = phone
    
    def set_human_info(human_id, hid_public_token, hid_access_token):
        self.human_id = human_id
        self.hid_public_token = hid_public_token
        self.hid_access_token = hid_access_token
    

class UsersSchema(Schema):
    __tablename__ = 'users'
    email = fields.Str()
    name = fields.Str()
    phone = fields.Str()
    human_id = fields.Str()
    hid_public_token = fields.Str()
    hid_access_token = fields.Str()


user_schema = UsersSchema()