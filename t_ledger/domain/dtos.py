from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)
from pydantic.alias_generators import to_camel

from t_ledger.domain.enums import (
    BondType,
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
        return self.units + self.nano / Decimal(1e9)


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
    asset_uid: str
    bond_type: BondType
    country_of_risk: str
    country_of_risk_name: str
    coupon_quantity_per_year: int
    currency: Currency
    name: str
    nominal: Money
    position_uid: str
    risk_level: RiskLevel
    sector: str
    uid: str


class Allocation(BaseDTO):
    active_instruments: list[InstrumentOut]
    currency: Currency
