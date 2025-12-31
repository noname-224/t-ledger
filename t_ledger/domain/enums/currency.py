from __future__ import annotations

from enum import StrEnum


class Currency(StrEnum):
    EUR = "EUR"
    RUB = "RUB"
    USD = "USD"
    NONE = ""

    @classmethod
    def from_api(cls, key: str) -> Currency:
        try:
            return _CURRENCY_MAP[key]
        except KeyError:
            raise ValueError(f"Unknown 'currency' api key: {key}")


_CURRENCY_MAP = {
    "eur": Currency.EUR,
    "rub": Currency.RUB,
    "usd": Currency.USD,
    "": Currency.NONE,
}
