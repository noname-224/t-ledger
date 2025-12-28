from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)
from pydantic.alias_generators import to_camel

from t_ledger.domain.enums import (
    CouponType,
    Currency,
    RiskLevel,
    InstrumentType,
)


class BaseDTO(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="ignore",
        validate_by_alias=True,
        validate_by_name=True,
    )


class Quantity(BaseDTO):
    units: Decimal
    nano: Decimal

    @property
    def value(self) -> Decimal:
        return self.units


class Money(BaseDTO):
    currency: Currency
    units: Decimal
    nano: Decimal

    @property
    def amount(self) -> Decimal:
        return self.units + self.nano / Decimal(1e9)


class Position(BaseDTO):
    position_uid: str
    instrument_uid: str
    instrument_type: str
    current_price: Money
    quantity: Quantity
    daily_yield: Money
    current_nkd: Money | None = None


class Instrument(BaseDTO):
    type: InstrumentType
    total_amount: Money


class InstrumentOut(Instrument):
    daily_yield: Decimal
    alloc_percent: Decimal


class Portfolio(BaseDTO):
    account_id: str
    positions: list[Position]
    total_amount_portfolio: Money
    daily_yield: Money
    instruments: list[Instrument]


class Bond(BaseDTO):
    country_of_risk: str
    currency: Currency
    name: str
    risk_level: RiskLevel
    uid: str
    quantity: Quantity | None = None


class Allocation(BaseDTO):
    active_instruments: list[InstrumentOut]
    currency: Currency


class Coupon(BaseDTO):
    bond_name: str
    quantity: Quantity
    coupon_date: datetime
    coupon_type: CouponType
    fix_date: datetime
    pay_one_bond: Money


class BondWithCoupons(BaseDTO):
    name: str
    quantity: Quantity
    coupons: list[Coupon]


class MonthlyCouponIncome(BaseDTO):
    month: int
    coupons: list[Coupon]
    total_income: Decimal


class AnnualCouponIncome(BaseDTO):
    year: int
    months: list[MonthlyCouponIncome]
    total_income: Decimal
