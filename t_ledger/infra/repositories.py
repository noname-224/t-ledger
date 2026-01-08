from typing import Any

from t_ledger.domain.contracts import CouponRepository


class InMemoryCouponRepository(CouponRepository):
    def __init__(self):
        self._data = {}

    async def update_data(self, chat_id: int, *, data: dict[str, Any] | None = None,
                          **kwargs) -> None:
        if data is not None:
            kwargs.update(data)

        self._data.setdefault(chat_id, {}).update(kwargs)

    async def get_data(self, chat_id: int) -> dict[str, Any] | None:
        return self._data.get(chat_id)
