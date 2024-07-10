from os import environ
import json
from fastapi import APIRouter, UploadFile, File, Security
from fastapi.responses import JSONResponse

from app.helpers.decorators import handleAPIError,logger
from app.controllers.extract import extract_arabic_english
from app.controllers.security import get_api_key
from app.config.constants import UPLOAD_DIR

if environ.get('DEBUG'):
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()

router = APIRouter()


@router.post("/arabic_english_document")
@handleAPIError
async def extract_arabic_english_doc(file: UploadFile = File(...),api_key: str = Security(get_api_key)):
    try: 
        pdf_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(pdf_path, "wb") as pdf:
            pdf.write(file.file.read())
        return await extract_arabic_english(pdf_path)
    except Exception as e:
        error_message = "Failed to load the data: " + str(e)
        return {"Status": False, "message": error_message}
