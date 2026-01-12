from datetime import datetime
from decimal import Decimal

from t_ledger.domain.enums.core import RiskLevel, CouponType
from t_ledger.domain.enums.core import Currency, InstrumentType
from t_ledger.domain.models.base import BaseModelConfig
from t_ledger.domain.models.value_objects import Money, Quantity


class Account(BaseModelConfig):
    id: int


class Position(BaseModelConfig):
    position_uid: str
    instrument_uid: str
    instrument_type: InstrumentType
    current_price: Money
    quantity: Quantity
    daily_yield: Money
    current_nkd: Money | None = None


class PositionBond(BaseModelConfig):
    instrument_uid: str
    quantity: Quantity


class TotalAmountByInstrument(BaseModelConfig):
    instrument_type: InstrumentType
    total_amount: Money


class PortfolioInstrumentAllocation(BaseModelConfig):
    instrument_type: InstrumentType
    total_amount: Money
    allocation_ratio: Decimal
    daily_yield: Money


class Portfolio(BaseModelConfig):
    account_id: str
    positions: list[Position]
    total_amount: Money
    daily_yield: Money
    total_amounts_by_instrument: list[TotalAmountByInstrument]


class Bond(BaseModelConfig):
    instrument_uid: str
    currency: Currency
    name: str
    country_of_risk: str
    risk_level: RiskLevel
    quantity: Quantity | None = None


class PortfolioAllocation(BaseModelConfig):
    instrument_allocations: list[PortfolioInstrumentAllocation]
    currency: Currency


class Coupon(BaseModelConfig):
    coupon_date: datetime
    coupon_type: CouponType
    amount_per_bond: Money

    bond_name: str | None = None
    bond_quantity: Quantity | None = None


class BondWithCouponSchedule(BaseModelConfig):
    instrument_uid: str
    coupons: list[Coupon]

    name: str | None = None
    quantity: Quantity | None = None


class MonthlyCouponIncome(BaseModelConfig):
    month: int
    total_income: Decimal
    coupons: list[Coupon]


class AnnualCouponIncome(BaseModelConfig):
    year: int
    total_income: Decimal
    monthly_incomes: list[MonthlyCouponIncome]


class BondsByRiskLevel(BaseModelConfig):
    risk_level: RiskLevel
    bonds: list[Bond]
