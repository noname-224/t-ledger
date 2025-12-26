from t_ledger.domain.enums import InstrumentType


instrument_types = {
    "totalAmountBonds": InstrumentType.BOND,
    "totalAmountCurrencies": InstrumentType.CURRENCY,
    "totalAmountEtf": InstrumentType.ETF,
    "totalAmountFutures": InstrumentType.FUTURE,
    "totalAmountOptions": InstrumentType.OPTION,
    "totalAmountShares": InstrumentType.SHARE,
    "totalAmountSp": InstrumentType.SP,
}

currency_to_sign = {
    "EUR": "€",
    "RUB": "₽",
    "USD": "$",
}
