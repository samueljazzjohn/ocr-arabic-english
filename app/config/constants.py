from os import getenv

TRAINED_DATA_URL= getenv('TRAINED_DATA_URL', '')
HOST= getenv('HOST', '')
SCHEME= getenv('SCHEME', '')
TRAINED_FILE_NAME="ara.traineddata"
UPLOAD_DIR="app/config/data/extracted_data"
SOURCE_DIR="app/config/data/source_data"