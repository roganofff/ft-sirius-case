import requests

from fastapi import APIRouter, Request
from openai import OpenAI
import httpx
from chatbot.config.settings import settings

from chatbot.src.models.schemas import ChatRequest, ChatResponse, SelectionRequest, SelectionResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)
client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Счётчики слабых матчей по IP
weak_counters = {}

@router.post("/api/v1/prompt", response_model=ChatResponse)
async def prompt(request: ChatRequest, raw: Request):
    user_text = request.message
    ip = raw.client.host
    weak_counters[ip] = weak_counters.get(ip, 0)

    try:
        # 1. Запрос к /match
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                "http://localhost:8000/api/requests/match",
                json={"description": user_text},
                timeout=30
            )
            resp.raise_for_status()
            matches = resp.json()

        logger.warning(f"Top matches: {matches}")

        if matches and matches[0]["score"] >= 0.7:
            weak_counters[ip] = 0
            return ChatResponse(
                reply=matches[0]["answer"],
                success=True
            )

        weak_counters[ip] += 1

        # Если подряд 3 слабых — вызвать GPT напрямую
        if weak_counters[ip] >= 3:
            weak_counters[ip] = 0
            gpt_reply = await ask_gpt(user_text, [])
            return ChatResponse(reply=gpt_reply, success=True)

        # Иначе — вызвать GPT с top-3
        top_answers = [m["answer"] for m in matches[:3]]
        gpt_reply = await ask_gpt(user_text, top_answers)
        return ChatResponse(reply=gpt_reply, success=True)

    except Exception as e:
        return ChatResponse(
            reply=f"Произошла ошибка: {str(e)}",
            success=False
        )


async def ask_gpt(user_question: str, top_answers: list[str]) -> str:
    if top_answers:
        system_prompt = (
            "Ты — помощник, который помогает жителям Сириуса. Вопрос от пользователя — внизу. Ниже даны 3 возможных ответа.\n"
            "1. Если один из них точно подходит — выбери его, скопируй как есть и верни.\n"
            "2. Если все 3 плохие — напиши ответ сам.\n"
            "Пиши коротко, без приветствий."
        )

        user_prompt = (
            f"Вопрос: {user_question}\n\n"
            "Возможные ответы:\n" +
            "\n".join(f"{i+1}. {a}" for i, a in enumerate(top_answers))
        )
    else:
        system_prompt = (
            "Ты — помощник, который помогает жителям Сириуса. Ответь на вопрос пользователя.\n"
            "Пиши коротко, без приветствий."
        )
        user_prompt = user_question

    request_body = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.5,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.LLM_PROXY_URL}/v1/chat/completions",
            json=request_body,
            headers=headers,
            timeout=60
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]