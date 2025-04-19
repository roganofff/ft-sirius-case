from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory='chatbot/src/templates')

@router.get("/", response_class=HTMLResponse)
async def welcome(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@router.get("/chat", response_class=HTMLResponse)
async def chat(request: Request):
    return templates.TemplateResponse('chat.html', {'request': request})