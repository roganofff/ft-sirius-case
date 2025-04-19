from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.templating import Jinja2Templates
from prometheus_fastapi_instrumentator import Instrumentator

from chatbot.src.api.routes.chat import router as chat_router
from chatbot.src.api.routes.prompt import router as prompt_router
from requests_api.src.app.routes.requests import router as requests_router
from requests_api.src.app.routes.similarity import router as similarity_router
import os

print(os.getcwd())
app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory='chatbot/src/static'),
    name="static"
)

app.add_middleware(
    CORSMiddleware,     # type: ignore[arg-type]
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(chat_router)
app.include_router(prompt_router)
app.include_router(requests_router)
app.include_router(similarity_router)
Instrumentator().instrument(app).expose(app)
