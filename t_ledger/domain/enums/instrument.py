from __future__ import annotations

from enum import StrEnum


class InstrumentType(StrEnum):
    BOND = "BOND"
    CURRENCY = "CURRENCY"
    ETF = "ETF"
    FUTURES = "FUTURES"
    OPTION = "OPTION"
    SHARE = "SHARE"
    SP = "SP"
    CLEARING_CERTIFICATE = "CLEARING_CERTIFICATE"
    INDEX = "INDEX"
    COMMODITY = "COMMODITY"

    @classmethod
    def from_api(cls, key: str) -> InstrumentType:
        try:
            return _INSTRUMENT_TYPE_MAP[key]
        except KeyError:
            raise ValueError(f"Unknown 'instrument' api key: {key}")


_INSTRUMENT_TYPE_MAP = {
    "totalAmountBonds": InstrumentType.BOND,
    "totalAmountCurrencies": InstrumentType.CURRENCY,
    "totalAmountEtf": InstrumentType.ETF,
    "totalAmountFutures": InstrumentType.FUTURES,
    "totalAmountOptions": InstrumentType.OPTION,
    "totalAmountShares": InstrumentType.SHARE,
    "totalAmountSp": InstrumentType.SP,
    "bond": InstrumentType.BOND,
    "share": InstrumentType.SHARE,
    "currency": InstrumentType.CURRENCY,
    "etf": InstrumentType.ETF,
    "futures": InstrumentType.FUTURES,
    "sp": InstrumentType.SP,
    "option": InstrumentType.OPTION,
    "clearing_certificate": InstrumentType.CLEARING_CERTIFICATE,
    "index": InstrumentType.INDEX,
    "commodity": InstrumentType.COMMODITY,
}
