import fitz
import pandas as pd
import pytesseract
import os

from pdf2image import convert_from_path
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from app.config.constants import HOST,SCHEME


async def extract_arabic_english(pdf_file):
    try:
        pages = convert_from_path(pdf_file)
        # Initialize an empty list to store the extracted text
        extracted_text = []

        # Loop through each page image
        for page_number, image in enumerate(pages, start=1):
            # Perform OCR to extract text from the image
            text =pytesseract.image_to_string(image , lang='ara+eng',config= ".")

            # Check if the extracted text is not empty
            if text.strip():
                extracted_text.append({"page": page_number, "text": text})

        if extracted_text:
            # Create a DataFrame from the extracted text
            df = pd.DataFrame(extracted_text)

            # Save the DataFrame to a CSV file
            output_csv_path = pdf_file.replace('.pdf', '.csv')
            df.to_csv(output_csv_path, index=False, encoding='utf-8')
            return JSONResponse(status_code=200, content={"message": f"You can download the extracted file from here: {SCHEME}://{HOST}/data/{output_csv_path.split('/')[-1]}."})
        else:
            return JSONResponse(status_code=200, content={"message": f"No text found in the PDF after OCR."})
    except Exception as e:
        error_message = f"Failed to download Tesseract data: {e}"
        raise HTTPException(status_code=500, detail=error_message)
        