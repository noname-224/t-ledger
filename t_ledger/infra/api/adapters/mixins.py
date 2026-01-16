from decimal import Decimal
from typing import Any

from t_ledger.domain.models.value_objects import Money, Quantity


class MoneyFieldDTOConverterMixin:
    def _money_convert(self, money_data: dict[str, Any]) -> Money:  # noqa
        return Money(
            amount=Decimal(money_data["units"]) + Decimal(money_data["nano"]) / Decimal("1e9"),
            currency=money_data["currency"],
        )


class QuantityFieldDTOConverterMixin:
    def _quantity_convert(self, quantity_data: dict[str, Any]) -> Money:  # noqa
        return Quantity(
            value=Decimal(quantity_data["units"]) + Decimal(quantity_data["nano"]) / Decimal("1e9")
        )
