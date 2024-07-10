import os

from fastapi import HTTPException, Security
from app.helpers.logger import logger
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.config.constants import *

API_KEY = SERVER_API_KEY
API_KEY_NAME = SERVER_API_KEY_NAME

if API_KEY is None or API_KEY_NAME is None:
    raise ValueError("SERVER_API_KEY and SERVER_KEY_NAME environment variables are not set")

def get_api_key(
        api_key_header: str = Security(
            APIKeyHeader(name=API_KEY_NAME, auto_error=False))) -> str:
    """
        Method help to verif the APIKEY in request
    """
    if api_key_header is None or api_key_header != API_KEY:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")
    return api_key_header