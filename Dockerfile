FROM python:3.9
WORKDIR /code
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install gunicorn

# Install Tesseract OCR and Poppler Utils
RUN apt-get update && \
    apt-get install -y tesseract-ocr poppler-utils && \
    apt-get install -y tesseract-ocr-eng tesseract-ocr-ara

COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80","--workers", "2"]
