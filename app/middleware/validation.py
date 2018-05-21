from aiohttp.web import HTTPForbidden
from ..lib.utils import parse_auth_header, match_request
from ..lib.tokens import decode_jwt_token
from ..lib.loggers import logger

def validation(ignore=None):
    async def factory(app, handler):
        async def middleware(request):
            auth = None 
            request_method = request.method
            request_path = request.rel_url.path

            if ignore and match_request(ignore, request_method, request_path):
                logger.debug( "skip route validation for: ", request_method + ":" + request_path )
                return await handler(request)

            if request.headers.get("Authorization"):
                auth = parse_auth_header(auth_type='jwt', auth_header=request.headers.get("Authorization"))
            token = request.cookies.get("token") or auth or None
            if token is not None:
                valid_token, error = decode_jwt_token(token)
                if error:
                    logger.error( "HTTPForbidden" )
                    raise HTTPForbidden(
                        reason=error,
                    )
                return await handler(request)
            else:
                logger.error( "HTTPForbidden" )
                raise HTTPForbidden(
                    reason='Invalid token scheme',
                )
            return await handler(request)
        return middleware
    return factory