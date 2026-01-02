from abc import ABC, abstractmethod
from typing import Any


class BaseCouponRepository(ABC):

    @abstractmethod
    async def update_data(self, chat_id: int, *, data: dict[str, Any] | None = None,
                          **kwargs) -> None:
        ...

    @abstractmethod
    async def get_data(self, chat_id: int) -> dict[str, Any] | None:
        ...
