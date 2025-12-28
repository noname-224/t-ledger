from aiogram import BaseMiddleware
from aiogram.types import Message

from t_ledger.config import settings


class AccessMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        if user_id in settings.tgbot.ids_allowed_users:
            return await handler(event, data)
        else:
            await event.answer("Доступ запрещен.")
            return None
