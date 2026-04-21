from abc import ABC, abstractmethod
from typing import Any

from t_ledger.domain.enums.core import MessageType


class MessageRepository(ABC):
    @abstractmethod
    async def get_message(self, message_type: MessageType) -> tuple[int, Any] | None: ...

    @abstractmethod
    async def save_message(
        self, message_type: MessageType, message_id: int, message_data: Any
    ) -> None: ...
