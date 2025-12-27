from enum import StrEnum


class Method(StrEnum):
    GET = "GET"
    POST = "POST"


class Endpoint(StrEnum):
    GET_ACCOUNTS = "/tinkoff.public.invest.api.contract.v1.UsersService/GetAccounts"
    GET_PORTFOLIO = "/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio"
    GET_BOND_BY = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/BondBy"
    GET_BOND_COUPONS = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/GetBondCoupons"


class Currency(StrEnum):
    EUR = "eur"
    RUB = "rub"
    USD = "usd"
    NONE = ""

class InstrumentType(StrEnum):
    BOND = "bond"
    CURRENCY = "currency"
    ETF = "etf"
    FUTURE = "future"
    OPTION = "option"
    SHARE = "share"
    SP = "sp"


class InstrumentIdType(StrEnum):
    UID = "INSTRUMENT_ID_TYPE_UID"


class RiskLevel(StrEnum):
    UNSPECIFIED = "RISK_LEVEL_UNSPECIFIED"
    LOW = "RISK_LEVEL_LOW"
    MODERATE = "RISK_LEVEL_MODERATE"
    HIGH = "RISK_LEVEL_HIGH"


class BondType(StrEnum):
    UNSPECIFIED = "BOND_TYPE_UNSPECIFIED"
    REPLACED = "BOND_TYPE_REPLACED"


class CouponType(StrEnum):
    UNSPECIFIED = "COUPON_TYPE_UNSPECIFIED"
    CONSTANT = "COUPON_TYPE_CONSTANT"
    FLOATING = "COUPON_TYPE_FLOATING"
    DISCOUNT = "COUPON_TYPE_DISCOUNT"
    MORTGAGE = "COUPON_TYPE_MORTGAGE"
    FIX = "COUPON_TYPE_FIX"
    VARIABLE = "COUPON_TYPE_VARIABLE"
    OTHER = "COUPON_TYPE_OTHER"
