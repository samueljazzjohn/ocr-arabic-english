from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import extract, train

app = FastAPI()

origins = [
    "*","https://extractor-dashboard.pivotpie.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    with open("/version.txt", 'r') as f:
        version = f.read().strip()
except BaseException:
    version = "0.0.0"


app.include_router(
    extract.router,
    prefix="/extract",
    tags=["Arabic + English Document Extraction"]
)

app.include_router(
    train.router,
    prefix="/train",
    tags=["Sync Trained dataset for Arabic"]
)
   
app.mount("/data", StaticFiles(directory="app/config/data"), name="data")
