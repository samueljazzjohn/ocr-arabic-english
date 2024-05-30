from os import environ
import json
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.helpers.decorators import handleAPIError,logger

if environ.get('DEBUG'):
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()

router = APIRouter()


@router.get("/")
@handleAPIError
async def extract_arabic_english_doc(file: UploadFile = File(...)):
    try: 
        return {"message": "Connection established successfully"}
    except Exception as e:
        error_message = "Failed to connect to talkingdb: " + str(e)
        return {"Status": False, "message": error_message}
