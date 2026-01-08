from aiogram import BaseMiddleware
from aiogram.types import Message

from t_ledger.presentation.telegram.texts.common import ACCESS_DENIED


class AccessMiddleware(BaseMiddleware):
    def __init__(self, allowed_user_ids: set[int]):
        self._allowed_user_ids = allowed_user_ids

    async def __call__(self, handler, event: Message, data):
        user_id = event.from_user.id
        if user_id in self._allowed_user_ids:
            return await handler(event, data)

        await event.answer(ACCESS_DENIED)
        return None
