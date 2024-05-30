import os
import requests

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.config.constants import TRAINED_DATA_URL,TRAINED_FILE_NAME



async def download_trained_data():
    try:
        # Download the file
        response = requests.get(TRAINED_DATA_URL)
        if response.status_code == 200:
            with open(TRAINED_FILE_NAME, "wb") as file:
                file.write(response.content)

            # Set the TESSDATA_PREFIX environment variable
            os.environ['TESSDATA_PREFIX'] = '/usr/share/tesseract-ocr/5/tessdata/'

            return JSONResponse(status_code=200, content={"message": f"Downloaded {TRAINED_FILE_NAME} successfully."})
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to download the file.")
    except Exception as e:
        error_message = f"Failed to download Tesseract data: {e}"
        raise HTTPException(status_code=500, detail=error_message)
        
    