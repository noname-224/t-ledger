from datetime import datetime
from decimal import Decimal

from t_ledger.domain.enums.core import RiskLevel, CouponType
from t_ledger.domain.enums.currency import Currency
from t_ledger.domain.enums.instrument import InstrumentType
from t_ledger.domain.models.base import BaseModelConfig
from t_ledger.domain.models.value_objects import Money, Quantity


class Position(BaseModelConfig):
    position_uid: str
    instrument_uid: str
    instrument_type: InstrumentType
    current_price: Money
    quantity: Quantity
    daily_yield: Money
    current_nkd: Money | None = None


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
    total_amounts_by_active_instrument: list[TotalAmountByInstrument]


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
    bond_name: str
    quantity: Quantity

    coupon_date: datetime
    coupon_type: CouponType
    amount_per_bond: Money


class BondWithCouponSchedule(BaseModelConfig):
    name: str
    quantity: Quantity
    coupons: list[Coupon]


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
