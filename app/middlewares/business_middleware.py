from typing import Callable, Dict, Any, Awaitable

import httpx
from aiogram import BaseMiddleware
from aiogram.dispatcher.middlewares.user_context import EventContext
from aiogram.types import TelegramObject, ChatFullInfo

from app.settings import secrets
from app.utils.opening_hours import check_opening_hours


class BusinessMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.telegram.org/bot{secrets.token}/getChat?"
                f"chat_id={secrets.admin_id}"
            )
            chat = response.json()
            full_chat = ChatFullInfo(**chat["result"])

            if check_opening_hours(full_chat.business_opening_hours):
                context: EventContext = data.get("event_context")

                if (
                        context.user.id != secrets.admin_id
                        and context.business_connection_id
                ):
                    return await handler(event, data)
