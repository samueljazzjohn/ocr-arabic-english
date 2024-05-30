from os import environ
import json
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

from app.helpers.decorators import handleAPIError,logger
from app.controllers.extract import extract_arabic_english
from app.config.constants import UPLOAD_DIR

if environ.get('DEBUG'):
    import debugpy
    debugpy.listen(5678)
    debugpy.wait_for_client()

router = APIRouter()


@router.get("/")
@handleAPIError
async def extract_arabic_english_doc(file: UploadFile = File(...)):
    try: 
        pdf_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(pdf_path, "wb") as pdf:
            pdf.write(file.file.read())
        return await extract_arabic_english(pdf_path)
    except Exception as e:
        error_message = "Failed to connect to talkingdb: " + str(e)
        return {"Status": False, "message": error_message}
