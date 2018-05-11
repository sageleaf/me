from app import db
from marshmallow import Schema, fields

class Nutrition(db.Model):
    __tablename__ = 'nutritional_data'
    nutritional_data_id = db.Column(db.VARCHAR(100), primary_key=True)
    profile_id = db.Column(db.VARCHAR(100))
    created_at = db.Column(db.DateTime)
    food_name = db.Column(db.VARCHAR(100))
    serving_qty = db.Column(db.VARCHAR(100))
    serving_unit = db.Column(db.VARCHAR(100))
    serving_weight_grams = db.Column(db.VARCHAR(100))
    calories = db.Column(db.VARCHAR(100))
    total_fat = db.Column(db.VARCHAR(100))
    saturated_fat = db.Column(db.VARCHAR(100))
    cholesterol = db.Column(db.VARCHAR(100))
    sodium = db.Column(db.VARCHAR(100))
    total_carbohydrate = db.Column(db.VARCHAR(100))
    dietary_fiber = db.Column(db.VARCHAR(100))
    sugars = db.Column(db.VARCHAR(100))
    protein = db.Column(db.VARCHAR(100))
    potassium = db.Column(db.VARCHAR(100))


    def __init__(self, *args):
        self.nutritional_data_id = args.nutritional_data_id
        self.profile_id = args.profile_id
        self.food_name = args.food_name
        self.serving_qty = args.serving_qty
        self.serving_unit = args.serving_unit
        self.serving_weight_grams = args.serving_weight_grams
        self.calories = args.nf_calories
        self.total_fat = args.nf_total_fat
        self.saturated_fat = args.nf_saturated_fat
        self.cholesterol = args.nf_cholesterol
        self.sodium = args.nf_sodium
        self.total_carbohydrate = args.nf_total_carbohydrate
        self.dietary_fiber = args.nf_dietary_fiber
        self.sugars = args.nf_sugars
        self.protein = args.nf_protein
        self.potassium = args.nf_potassium


    def commit(self):
        db.session.add(self)
        db.session.commit()


class NutritionSchema(Schema):
    __tablename__ = 'nutritional_data'
    nutritional_data_id = fields.Str()
    profile_id = fields.Str()
    created_at = fields.Str()
    food_name = fields.Str()
    serving_qty = fields.Str()
    serving_unit = fields.Str()
    serving_weight_grams = fields.Str()
    calories = fields.Str()
    total_fat = fields.Str()
    saturated_fat = fields.Str()
    cholesterol = fields.Str()
    sodium = fields.Str()
    total_carbohydrate = fields.Str()
    dietary_fiber = fields.Str()
    sugars = fields.Str()
    protein = fields.Str()
    potassium = fields.Str()


nutrition_schema = NutritionSchema()