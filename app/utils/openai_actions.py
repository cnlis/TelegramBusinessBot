import httpx
from aiogram.types import Message
from openai import AsyncOpenAI

from app.settings import secrets
from app.views import system_prompt


async def get_chat_completion(message: Message):
    http_client = httpx.AsyncClient(
        limits=httpx.Limits(
            max_connections=100, max_keepalive_connections=20)
    )
    client = AsyncOpenAI(
        api_key=secrets.openai_key,
        http_client=http_client,
        base_url=secrets.openai_base_url,
    )

    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": message.text},
    ]

    response = await client.chat.completions.create(
        model="gpt-4o", messages=messages, max_tokens=1000, temperature=0.8,
    )

    return response.choices[0].message.content