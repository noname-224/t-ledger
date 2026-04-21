from enum import StrEnum


class InstrumentType(StrEnum):
    BOND = "bond"
    CURRENCY = "currency"
    ETF = "etf"
    FUTURES = "futures"
    OPTION = "option"
    SHARE = "share"
    SP = "sp"
    CLEARING_CERTIFICATE = "clearing_certificate"
    INDEX = "index"
    COMMODITY = "commodity"


class Currency(StrEnum):
    EUR = "eur"
    RUB = "rub"
    USD = "usd"
    NONE = ""


class RiskLevel(StrEnum):
    LOW = "RISK_LEVEL_LOW"
    MODERATE = "RISK_LEVEL_MODERATE"
    HIGH = "RISK_LEVEL_HIGH"
    UNSPECIFIED = "RISK_LEVEL_UNSPECIFIED"


class CouponType(StrEnum):
    UNSPECIFIED = "COUPON_TYPE_UNSPECIFIED"
    CONSTANT = "COUPON_TYPE_CONSTANT"
    FLOATING = "COUPON_TYPE_FLOATING"
    DISCOUNT = "COUPON_TYPE_DISCOUNT"
    MORTGAGE = "COUPON_TYPE_MORTGAGE"
    FIX = "COUPON_TYPE_FIX"
    VARIABLE = "COUPON_TYPE_VARIABLE"
    OTHER = "COUPON_TYPE_OTHER"


class MessageType(StrEnum):
    FUTURE_BOND_PAYMENTS = "FUTURE_BOND_PAYMENTS"
