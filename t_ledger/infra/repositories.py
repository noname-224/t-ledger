from datetime import datetime, timezone, timedelta
from typing import Any

from t_ledger.domain.enums.core import MessageType
from t_ledger.domain.interfaces.repositories import MessageRepository


class InMemoryMessageRepository(MessageRepository):
    def __init__(self, ttl: timedelta = timedelta(minutes=5)):
        self._ttl = ttl
        self._storage: dict[str, tuple[int, Any, datetime]] = {}

    async def get_message(self, message_type: MessageType) -> tuple[int, Any] | None:
        data = self._storage.get(message_type)
        if data is None:
            return None

        message_id, message_data, saved_at = data
        if saved_at + self._ttl < datetime.now(timezone.utc):
            del self._storage[message_type]
            return None

        return message_id, message_data

    async def save_message(
        self, message_type: MessageType, message_id: int, message_data: Any
    ) -> None:
        self._storage[message_type] = (message_id, message_data, datetime.now(timezone.utc))
