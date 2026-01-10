from __future__ import annotations

from decimal import Decimal
from typing import Any

from pydantic import Field

from t_ledger.domain.enums.core import Currency
from t_ledger.domain.models.base import BaseModelConfig


class Quantity(BaseModelConfig):
    value: Decimal = Field(..., ge=0)

    @classmethod
    def from_api(cls, raw: dict) -> Quantity:
        return cls(
            value=Decimal(raw["units"]) + Decimal(raw["nano"]) / Decimal("1e9"),
        )


class Money(BaseModelConfig):
    amount: Decimal
    currency: Currency

    def __add__(self, other):
        self._check_other(other)

        return Money(amount=self.amount + other.amount, currency=self.currency)

    def __iadd__(self, other):
        self._check_other(other)

        self.amount += other.amount
        return self

    @classmethod
    def from_api(cls, raw: dict | None) -> Money:
        if raw is None:
            return None
        return cls(
            amount=Decimal(raw["units"]) + Decimal(raw["nano"]) / Decimal("1e9"),
            currency=raw["currency"],
        )

    @property
    def is_positive(self) -> bool:
        return self.amount > Decimal("0")

    def _check_other(self, other: Any) -> None:
        if not isinstance(other, Money):
            raise TypeError(
                f"Cannot add object of type {type(other).__name__!r} to {type(self).__name__!r}"
            )
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add objects with different currencies: {other.currency}, {self.currency}"
            )
