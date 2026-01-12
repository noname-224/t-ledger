from __future__ import annotations

from decimal import Decimal

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
