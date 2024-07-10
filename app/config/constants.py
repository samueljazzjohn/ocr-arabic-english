from os import getenv

TRAINED_DATA_URL= getenv('TRAINED_DATA_URL', '')
HOST= getenv('HOST', '')
SCHEME= getenv('SCHEME', '')
TRAINED_FILE_NAME="ara.traineddata"
UPLOAD_DIR="app/config/data/extracted_data"
SOURCE_DIR="app/config/data/source_data"
SERVER_API_KEY_NAME=getenv('SERVER_API_KEY_NAME', 'API-KEY')
SERVER_API_KEY=getenv('SERVER_API_KEY', '')
GPT_BEARER_TOKEN=getenv('GPT_BEARER_TOKEN', '')
LLM_MODEL=getenv('LLM_MODEL', '')
LLM_TEMPERATURE=getenv('LLM_TEMPERATURE')