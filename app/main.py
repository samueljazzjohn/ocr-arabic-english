from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.routers import extract

app = FastAPI()

origins = [
    "*"
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
   
