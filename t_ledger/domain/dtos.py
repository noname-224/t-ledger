from decimal import Decimal

from pydantic import BaseModel, ConfigDict, model_validator, Field, AliasPath
from pydantic.alias_generators import to_camel

from t_ledger.constants import Currency, AssetCategory, RiskLevel


class BaseDTOExtraAllow(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="allow",
        validate_by_alias=True,
        validate_by_name=True,
    )


class BaseDTOExtraIgnore(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="ignore",
        validate_by_alias=True,
        validate_by_name=True,
    )


class QuantityDTO(BaseDTOExtraIgnore):
    units: int
    nano: int

    @property
    def as_decimal(self) -> Decimal:
        return Decimal(self.units) + Decimal(self.nano) / Decimal(1e9)


class MoneyDTO(BaseDTOExtraIgnore):
    currency: Currency
    units: int
    nano: int

    @property
    def as_decimal(self) -> Decimal:
        return Decimal(self.units) + Decimal(self.nano) / Decimal(1e9)


class PositionDTO(BaseDTOExtraIgnore):
    position_uid: str
    instrument_uid: str
    instrument_type: str
    quantity: QuantityDTO
    current_price: MoneyDTO


class AmountByCategoryDTO(BaseDTOExtraIgnore):
    category: str
    amount: MoneyDTO


class PortfolioDTO(BaseDTOExtraAllow):
    total_amount_portfolio: MoneyDTO
    positions: list[PositionDTO]
    amounts_by_category: list[AmountByCategoryDTO] = []

    @model_validator(mode="after")
    def collect_total_amounts_by_category(self) -> "PortfolioDTO":
        category_mapping = {
            "totalAmountBonds": "bonds",
            "totalAmountCurrencies": "currencies",
            "totalAmountEtf": "etf",
            "totalAmountFutures": "futures",
            "totalAmountOptions": "options",
            "totalAmountShares": "shares",
            "totalAmountSp": "sp",
        }

        collected: list[AmountByCategoryDTO] = []
        extra = self.model_extra or {}

        for field_name, category in category_mapping.items():
            if raw_amount := extra.get(field_name):
                amount = MoneyDTO.model_validate(raw_amount)
                collected.append(AmountByCategoryDTO(category=category, amount=amount))

        self.amounts_by_category = collected
        self.model_extra.clear()

        return self


class CategoryInfoDTO(BaseDTOExtraIgnore):
    amount: Decimal
    category: AssetCategory
    currency: Currency
    percentage: Decimal


class BondInfoDTO(BaseDTOExtraIgnore):
    uid: str = Field(validation_alias=AliasPath("instrument", "uid"))
    name: str = Field(validation_alias=AliasPath("instrument", "name"))
    risk_level: RiskLevel = Field(validation_alias=AliasPath("instrument", "riskLevel"))

    @property
    def risk_level_ru(self) -> str:
        mapping = {
            "RISK_LEVEL_UNSPECIFIED": "⚪️ не указан",
            "RISK_LEVEL_LOW": "🟢 низкий",
            "RISK_LEVEL_MODERATE": "🟡 средний",
            "RISK_LEVEL_HIGH": "🔴 высокий",
        }
        return mapping.get(self.risk_level, "⚠️ неизвестно")
