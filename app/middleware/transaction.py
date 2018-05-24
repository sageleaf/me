from aiohttp.web import json_response
from ..lib.utils import parse_auth_header, match_request
from ..lib.tokens import decode_jwt_token
from ..lib.loggers import logger
from ..constants.errors import generate_error

async def transaction(app, handler):
    async def middleware(request):
        if request.method == "OPTIONS":
                return await handler(request)

        # we have the header its all good
        sage_leaf_tid = request.headers.get("sage_leaf_tid", None)
        if sage_leaf_tid is not None:
            return await handler(request)
        
        query_string = request.rel_url.query
        query_tid = query_string.get("sage_leaf_tid", None)
        if query_tid is not None:
            request.headers["sage_leaf_tid"] = query_tid
            return await handler(request)
        else:
            return json_response(generate_error('invalid_header', detail="sage_leaf_tid is required in all requests"), status=400)
    return middleware
