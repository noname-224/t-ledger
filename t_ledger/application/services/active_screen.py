from typing import Any

from t_ledger.domain.enums.core import MessageType
from t_ledger.domain.interfaces.repositories import MessageRepository
from t_ledger.domain.interfaces.services import ActiveMessageService


class ActiveMessageServiceImpl(ActiveMessageService):
    def __init__(self, message_repo: MessageRepository):
        self._message_repo = message_repo

    async def get_active_message(self, message_type: MessageType) -> tuple[int, Any] | None:
        return await self._message_repo.get_message(message_type)

    async def set_active_message(
        self, message_type: MessageType, message_id: int, message_data: Any
    ) -> None:
        await self._message_repo.save_message(message_type, message_id, message_data)
