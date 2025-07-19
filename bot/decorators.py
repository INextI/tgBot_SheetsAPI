from functools import wraps
from aiogram.types import Message
from typing import Callable, Awaitable, Any
from .create_bot import ADMINS_ID

def admin_only(handler: Callable[[Message], Awaitable[Any]]):
    @wraps(handler)
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id in ADMINS_ID:
            return await handler(message, *args, **kwargs)
        else:
            await message.answer("⛔ У вас нет доступа к этой команде.")
    return wrapper