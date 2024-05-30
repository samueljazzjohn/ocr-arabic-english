from os import environ
import json
from fastapi import APIRouter, HTTPException

from app.controllers.train import download_trained_data

from app.helpers.decorators import handleAPIError,logger

if environ.get('DEBUG'):
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()

router = APIRouter()


@router.post("/")
async def sync_trained_data_with_model():
    try:
        return await download_trained_data()
    except Exception as e:
        error_message = f"Failed to download Tesseract data: {e}"
        raise HTTPException(status_code=500, detail=error_message)