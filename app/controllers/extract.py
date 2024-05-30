import fitz
import pandas as pd
import pytesseract
import os

from pdf2image import convert_from_path
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool

from app.config.constants import HOST, SCHEME

async def extract_arabic_english(pdf_file: str):
    try:
        # Convert PDF to images asynchronously
        pages = await run_in_threadpool(convert_from_path, pdf_file)
        
        extracted_text = []

        for page_number, image in enumerate(pages, start=1):
            # Perform OCR to extract text from the image asynchronously
            text = await run_in_threadpool(pytesseract.image_to_string, image, lang='ara+eng', config='.')

            if text.strip():
                extracted_text.append({"page": page_number, "text": text})

        if extracted_text:
            df = pd.DataFrame(extracted_text)
            output_csv_path = pdf_file.replace('.pdf', '.csv')
            await run_in_threadpool(df.to_csv, output_csv_path, index=False, encoding='utf-8')

            return JSONResponse(
                status_code=200,
                content={"message": f"You can download the extracted file from here: {SCHEME}://{HOST}/data/extracted_data/{output_csv_path.split('/')[-1]}."}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"message": "No text found in the PDF after OCR."}
            )
    except Exception as e:
        error_message = f"Failed to process the PDF: {e}"
        raise HTTPException(status_code=500, detail=error_message)