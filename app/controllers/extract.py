import fitz
import pandas as pd
import pytesseract
import os
import asyncio
import decimal

from pdf2image import convert_from_path
from openai import OpenAI
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from concurrent.futures import ThreadPoolExecutor

from app.config.constants import HOST, SCHEME, GPT_BEARER_TOKEN, LLM_MODEL, LLM_TEMPERATURE

client = OpenAI(api_key=GPT_BEARER_TOKEN)

def ocr_page(image, page_number):
    text = pytesseract.image_to_string(image, lang='ara+eng', config='.')
    if text.strip():
        return {"page": page_number, "text": text}
    return None

async def translate_text(text):
    LLM_TEMPERATURE_DECIMAL = decimal.Decimal(LLM_TEMPERATURE)
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            temperature=float(LLM_TEMPERATURE_DECIMAL),
            messages=[
                    {"role": "user", "content": f"Translate the following text from Arabic and English to English:\n\ {text}"},
                ],
        )
        translated_text = response.choices[0].message.content
        return translated_text
    except Exception as e:
        print(f"Translation failed: {e}")
        return None

async def extract_arabic_english(pdf_file: str):
    try:
        # Convert PDF to images asynchronously
        pages = await run_in_threadpool(convert_from_path, pdf_file)

        if len(pages) > 3:
            return JSONResponse(
                status_code=400,
                content={"message": "We are not supporting morethan 3 pages now."}
            )
        
        # Use ThreadPoolExecutor for parallel processing of pages
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(ocr_page, image, page_number) for page_number, image in enumerate(pages, start=1)]
            results = [future.result() for future in futures]

        # Filter out None results (pages with no text)
        extracted_text = [result for result in results if result is not None]

        if extracted_text:
            df = pd.DataFrame(extracted_text)

            # Translate individual pages
            # df['translated_text'] = await asyncio.gather(*[translate_text(row['text']) for _, row in df.iterrows()])

            # Concatenate all texts for the final translation
            all_text = "\n\n".join(df['text'].tolist())
            final_translation = await translate_text(all_text)

            # Add a single row for the entire document's translation
            df.loc[len(df)] = {'page': 'Translated Text', 'text': final_translation}

            output_csv_path = pdf_file.replace('.pdf', '.csv')
            await run_in_threadpool(df.to_csv, output_csv_path, index=False, encoding='utf-8')

            return JSONResponse(
                status_code=200,
                content={"message": f"You can download the extracted file from here: {SCHEME}://{HOST}/data/extracted_data/{output_csv_path.split('/')[-1]}.", "file": f"{SCHEME}://{HOST}/data/extracted_data/{output_csv_path.split('/')[-1]}"}
            )
        else:
            return JSONResponse(
                status_code=200,
                content={"message": "No text found in the PDF after OCR."}
            )
    except Exception as e:
        error_message = f"Failed to process the PDF: {e}"
        raise HTTPException(status_code=500, detail=error_message)