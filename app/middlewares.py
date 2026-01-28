from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import Message

from app.database.models import User

class Ban_check(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]) -> Any:
        user = await User.get_or_none(tg_id=event.from_user.id)
        if user and user.block:
            if isinstance(event, Message):
                await event.answer("Вы заблокированы и не можете пользоваться функциями бота!")
            return 

        result = await handler(event, data)
        return result
        