import traceback
from functools import wraps

from app.helpers.logger import logger
from fastapi import HTTPException


def handleAPIError(route):
    '''Decorator that handles API route error.'''

    @wraps(route)
    async def wrap(*args, **kwargs):
        try:
            return await route(*args, **kwargs)
        except Exception as e:
            logger.info({"args": args, "kwargs": kwargs})
            logger.exception(e)
            raise HTTPException(status_code=500, detail={"message": "Internal Server Error",
                                                         "error": traceback.format_exc()})
    return wrap
