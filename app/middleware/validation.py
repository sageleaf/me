from aiohttp.web import json_response
from ..lib.utils import parse_auth_header, match_request
from ..lib.tokens import decode_jwt_token
from ..lib.loggers import logger
from ..constants.errors import generate_error

def validation(ignore=None):
    async def factory(app, handler):
        async def middleware(request):
            auth = None 
            request_method = request.method
            request_path = request.rel_url.path

            if request.method == "OPTIONS":
                return await handler(request)

            if ignore and match_request(ignore, request_method, request_path):
                # logger.debug( "skip route validation for: ", request_method + ":" + request_path )
                return await handler(request)

            if request.headers.get("Authorization"):
                auth = parse_auth_header(auth_type='jwt', auth_header=request.headers.get("Authorization"))

            token = request.cookies.get("token", auth)

            if token is not None:
                valid_token, token_error = decode_jwt_token(token)

                if token_error:
                    return json_response(generate_error('jwt_error', detail=token_error), status=400)
                # TODO: research other options... not sure I like adding this to headers. 
                request.headers["profile_id"] = valid_token
                return await handler(request)
            else:
                return json_response(generate_error('jwt_error', detail='Invalid token scheme'), status=400)
            return await handler(request)
        return middleware
    return factory