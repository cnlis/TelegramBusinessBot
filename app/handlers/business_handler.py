import asyncio

from aiogram.types import Message

from app.settings import redis_conn
from app.utils.check_delay import check_user_delay
from app.utils.openai_actions import get_chat_completion


async def handle_business_message(message: Message):
    if await check_user_delay(message.from_user.id) and message.text:
        answer = await get_chat_completion(message)
        await message.reply(answer)
        await redis_conn.set(
            f"users:{message.from_user.id}", asyncio.get_event_loop().time()
        )
