from decimal import Decimal

from pydantic import Field

from t_ledger.domain.enums.core import Currency
from t_ledger.domain.models.base import BaseModelConfig


class Quantity(BaseModelConfig):
    value: Decimal = Field(..., ge=0)


class Money(BaseModelConfig):
    amount: Decimal
    currency: Currency

    @property
    def is_positive(self) -> bool:
        return self.amount > Decimal("0")
