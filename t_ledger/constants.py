from enum import StrEnum


class Method(StrEnum):
    GET = "GET"
    POST = "POST"


class Endpoint(StrEnum):
    GET_ACCOUNTS = "/tinkoff.public.invest.api.contract.v1.UsersService/GetAccounts"
    GET_PORTFOLIO = "/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio"
    GET_BOND_BY = "/tinkoff.public.invest.api.contract.v1.InstrumentsService/BondBy"


class Currency(StrEnum):
    EUR = "eur"
    RUB = "rub"
    USD = "usd"


class AssetCategory(StrEnum):
    BONDS = "bonds"
    CURRENCIES = "currencies"
    ETF = "etf"
    FUTURES = "futures"
    OPTIONS = "options"
    SHARES = "shares"
    SP = "sp"


class InstrumentType(StrEnum):
    BOND = "bond"
    CURRENCY = "currency"
    ETF = "etf"
    FUTURE = "future"
    OPTION = "option"
    SHARE = "share"
    SP = "sp"


class IdType(StrEnum):
    UID = "INSTRUMENT_ID_TYPE_UID"


class RiskLevel(StrEnum):
    RISK_LEVEL_UNSPECIFIED = "RISK_LEVEL_UNSPECIFIED"
    RISK_LEVEL_LOW = "RISK_LEVEL_LOW"
    RISK_LEVEL_MODERATE = "RISK_LEVEL_MODERATE"
    RISK_LEVEL_HIGH = "RISK_LEVEL_HIGH"
