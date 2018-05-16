from app import db
from marshmallow import Schema, fields


class Vitals(db.Model):
    __tablename__ = 'manual_data'
    manual_data_id = db.Column(db.VARCHAR(100), primary_key=True)
    profile_id = db.Column(db.VARCHAR(100))
    created_at = db.Column(db.DateTime)
    data_key = db.Column(db.VARCHAR(100))
    data_value = db.Column(db.VARCHAR(100))
    performed_at = db.Column(db.DateTime)


    def __init__(self, manual_data_id, profile_id, created_at, data_key, data_value, performed_at):
        self.manual_data_id = manual_data_id
        self.profile_id = profile_id
        self.created_at = created_at
        self.data_key = data_key
        self.data_value = data_value
        self.performed_at = performed_at
    

    def commit(self):
        db.session.add(self)
        db.session.commit()


class VitalsSchema(Schema):
    __tablename__ = 'manual_data'
    manual_data_id = fields.Str()
    profile_id = fields.Str()
    created_at = fields.Str()
    data_key = fields.Str()
    data_value = fields.Str()
    performed_at = fields.Str()


vitals_schema = VitalsSchema()

