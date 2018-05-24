from aiohttp.web import json_response
from ..constants.errors import generate_error
from sqlalchemy import Column, String, DateTime
from marshmallow import Schema, fields
from ..lib.database import Base, session

async def validate_app(app, handler):
    async def middleware(request):

        req_app_id  = request.headers.get("app_id")
        req_api_key = request.headers.get("api_key")
        
        application = Applications.query.filter_by(app_id=req_app_id).first()
        data, error = ApplicationsSchema().dump(application)
        if error:
            return json_response(generate_error('data_retrieval', detail=None), status=500)

        api_key     = data.get("api_key", None)
        if api_key is None or api_key != req_api_key:
            return json_response(generate_error('invalid_application', detail=None), status=401)

        return await handler(request)
    return middleware



class Applications(Base):
    __tablename__ = 'applications'
    app_id = Column(String(45), primary_key=True)
    api_key = Column(DateTime)
    created_at = Column(DateTime)

    def __init__(self, app_id, api_key, created_at):
        self.app_id = app_id
        self.api_key = api_key
        self.created_at = created_at
    
    def commit(self):
        session.add(self)
        session.commit()
    

class ApplicationsSchema(Schema):
    __tablename__ = 'applications'
    app_id = fields.Str()
    api_key = fields.Str()
    created_at = fields.Str()