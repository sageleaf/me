from datetime import datetime
from aiohttp import ClientSession, TCPConnector
from .loggers import logger

# TODO: handle error scenarios
async def fetch(url="", method="GET", headers={}, data=None, req={}):
    _method = method.lower()
    tid = req.headers.get("sage_leaf_tid")
    session = ClientSession(connector=TCPConnector(verify_ssl=False))
    caller = getattr(session, _method)
    async with session:
            start = datetime.utcnow()
            async with caller(url, headers=headers, json=data) as response:
                time = start - datetime.utcnow()
                logger.info("[DOWNSTREAM REQUEST]: method=" + method +
                    " url=" + url +
                    " sage_leaf_tid=" + tid +
                    " status=" + str(response.status) +
                    " time=" + str(time.microseconds/1000) )
                return await response.json()