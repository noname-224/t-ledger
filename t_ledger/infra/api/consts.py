from datetime import datetime, timezone, timedelta

INSTRUMENT_TYPES = {
    "totalAmountBonds": "bond",
    "totalAmountCurrencies": "currency",
    "totalAmountEtf": "etf",
    "totalAmountFutures": "futures",
    "totalAmountOptions": "option",
    "totalAmountShares": "share",
    "totalAmountSp": "sp",
}
INSTRUMENT_ID_TYPE_UID = "INSTRUMENT_ID_TYPE_UID"
COUPONS_BY_BONDS_END_DATE = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
