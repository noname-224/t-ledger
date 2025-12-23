from dataclasses import dataclass
from decimal import Decimal

from t_ledger.constants import Currency, AssetCategory


@dataclass(frozen=True, slots=True)
class Money:
    amount: Decimal
    currency: Currency


@dataclass(frozen=True, slots=True)
class Quantity:
    value: Decimal


@dataclass(frozen=True, slots=True)
class AmountByCategory:
    category: AssetCategory
    amount: Money


@dataclass(frozen=True, slots=True)
class Position:
    uid: str
    instrument_uid: str
    instrument_type: str

    quantity: Quantity
    current_price: Money | None = None


@dataclass(frozen=True, slots=True)
class Portfolio:
    total_amount: Money
    amounts_by_category: list[AmountByCategory]
    positions: list[Position]
