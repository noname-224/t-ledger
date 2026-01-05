from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RawAccount:
    id: str


@dataclass(slots=True)
class RawPosition:
    position_uid: str
    instrument_uid: str
    instrument_type: str
    current_price: dict[str, Any]
    quantity: dict[str, Any]
    daily_yield: dict[str, Any]
    current_nkd: dict[str, Any] | None


@dataclass(slots=True)
class RawPortfolio:
    account_id: str
    positions: list[RawPosition]
    total_amount: dict[str, Any]
    daily_yield: dict[str, Any]
    total_amounts_by_instrument: dict[str, Any]


@dataclass(slots=True)
class RawBond:
    instrument_uid: str
    currency: str
    name: str
    risk_level: str
    country_of_risk: str


@dataclass(slots=True)
class RawCoupon:
    coupon_date: str
    coupon_type: str
    amount_per_bond: dict[str, Any]


@dataclass(slots=True)
class RawBondWithCoupons:
    instrument_uid: str
    coupons: list[RawCoupon]
