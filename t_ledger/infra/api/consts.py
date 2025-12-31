from datetime import datetime, timezone, timedelta

INSTRUMENT_TYPES = [
    "totalAmountBonds",
    "totalAmountCurrencies",
    "totalAmountEtf",
    "totalAmountFutures",
    "totalAmountOptions",
    "totalAmountShares",
    "totalAmountSp",
]
INSTRUMENT_ID_TYPE_UID = "INSTRUMENT_ID_TYPE_UID"
COUPONS_BY_BONDS_END_DATE = (datetime.now(timezone.utc) + timedelta(days=365)).isoformat()
