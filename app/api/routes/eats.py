from aiohttp.web import json_response
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from marshmallow import Schema, fields
from ...constants.errors import generate_error
from config import (NUTRITIONIX_APP_ID,
    NUTRITIONIX_APP_KEY,
    NUTRITIONIX_BASE_URL,
    NUTRITIONIX_PATH_NUTRIENTS,
    NUTRITIONIX_PATH_SEARCH,
    NUTRITIONIX_PATH_SEARCH_ITEM)
from ...lib.database import Base, session
from ...lib.fetch import fetch
from ...lib.utils import generate_uuid

NUTRITIONIX_HEADERS  = {
    "x-app-id": NUTRITIONIX_APP_ID,
    "x-app-key": NUTRITIONIX_APP_KEY
}


# route handlers
async def handle_add_eats(request) -> json_response:
    '''
        in: list of strings ->
            food_name
    '''
    post_body = await request.json()
    if not isinstance(post_body, list):
        return json_response(generate_error('invalid_request', detail="please send in list format []"), status=401)

    data = { "query": " and ".join(post_body) }
    url=NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_NUTRIENTS
    response = await fetch(url=url, method="POST", headers=NUTRITIONIX_HEADERS, data=data, req=request)
    foods = response.get("foods", None)
    profile_id = request.headers.get("profile_id", None)
    if profile_id is None:
        return json_response(generate_error('need_more_info', detail="invalid profile"), status=400)
    
    if foods is not None:
        run_time = str(datetime.utcnow())
        for food in foods:
            new_food = Ingredients(generate_uuid(), profile_id, run_time, food)
            new_food.commit()
        return json_response(status=204)
    else:
        return json_response(generate_error('not_found', detail=None), status=404)


async def handle_get_eats(request) -> json_response:
    profile_id = request.headers.get("profile_id", None)
    if profile_id is None:
        return json_response(generate_error('need_more_info', detail="invalid profile"), status=400)

    ingredients = Ingredients.query.filter_by(profile_id=profile_id).all()
    dump = []
    for ingredeint in ingredients:
        # ignore errors for now
        ingredient_dump, ingredeint_error = IngredientsSchema().dump(ingredeint)
        dump.append(ingredient_dump)
    return json_response(dump)


async def handle_browse_eats(request) -> json_response:
    query_string = request.rel_url.query
    query = query_string["query"]
    if query is None: 
        return json_response(generate_error('need_more_info', detail="please provide an item to `query`"), status=400)

    data = { "query": query }
    url=NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_NUTRIENTS
    response = await fetch(url=url, method="POST", headers=NUTRITIONIX_HEADERS, data=data, req=request)
    food_names = list(map(lambda food: food["food_name"], response.get("foods", [])))
    return json_response(food_names)


async def handle_search_eats(request) -> json_response:
    query_string = request.rel_url.query
    query = query_string["query"]
    if query is None: 
        return json_response(generate_error('need_more_info', detail="please provide an item to `query`"), status=400)

    url = NUTRITIONIX_BASE_URL + NUTRITIONIX_PATH_SEARCH + "?branded=false&query=" + query
    response = await fetch(url=url, method="GET", headers=NUTRITIONIX_HEADERS, req=request)
    return json_response(response)


# database schemas
class Ingredients(Base):
    __tablename__ = 'ingredients'
    ingredient_id = Column(String(100), primary_key=True)
    profile_id = Column(String(100))
    created_at = Column(DateTime)
    food_name = Column(String(100))
    serving_qty = Column(String(100))
    serving_unit = Column(String(100))
    serving_weight_grams = Column(String(100))
    calories = Column(String(100))
    total_fat = Column(String(100))
    saturated_fat = Column(String(100))
    cholesterol = Column(String(100))
    sodium = Column(String(100))
    total_carbohydrate = Column(String(100))
    dietary_fiber = Column(String(100))
    sugars = Column(String(100))
    protein = Column(String(100))
    potassium = Column(String(100))


    def __init__(self, ingredient_id, profile_id, created_at, params):
        self.ingredient_id = ingredient_id
        self.profile_id = profile_id
        self.created_at = created_at
        self.food_name = params["food_name"]
        self.serving_qty = params["serving_qty"]
        self.serving_unit = params["serving_unit"]
        self.serving_weight_grams = params["serving_weight_grams"]
        self.calories = params["nf_calories"]
        self.total_fat = params["nf_total_fat"]
        self.saturated_fat = params["nf_saturated_fat"]
        self.cholesterol = params["nf_cholesterol"]
        self.sodium = params["nf_sodium"]
        self.total_carbohydrate = params["nf_total_carbohydrate"]
        self.dietary_fiber = params["nf_dietary_fiber"]
        self.sugars = params["nf_sugars"]
        self.protein = params["nf_protein"]
        self.potassium = params["nf_potassium"]


    def commit(self):
        session.add(self)
        session.commit()


class IngredientsSchema(Schema):
    __tablename__ = 'nutritional_data'
    ingredient_id = fields.Str()
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