from decimal import Decimal

from t_ledger.domain.enums.core import Currency
from t_ledger.presentation.shared.formatting.ui import (
    bold,
    monospace,
    cut_line,
    currency_sign,
    underlined,
)

MONTH_NAMES = {
    1: "ЯНВАРЬ",
    2: "ФЕВРАЛЬ",
    3: "МАРТ",
    4: "АПРЕЛЬ",
    5: "МАЙ",
    6: "ИЮНЬ",
    7: "ИЮЛЬ",
    8: "АВГУСТ",
    9: "СЕНТЯБРЬ",
    10: "ОКТЯБРЬ",
    11: "НОЯБРЬ",
    12: "ДЕКАБРЬ",
}


def format_month_title(year: int, month: int) -> str:
    return f"{bold(year)} {underlined(bold(MONTH_NAMES.get(month, '...')))}"


def format_coupon_line(
    *,
    day: int,
    name: str,
    amount: Decimal,
    currency: Currency,
    max_name_len: int = 12,
    max_amount_len: int = 10,
) -> str:
    day = f"{day:02d}"
    name = f"{cut_line(name)}"
    sign = currency_sign(currency)

    return monospace(f"{day} | {name:<{max_name_len}} | {amount:>{max_amount_len},.2f}{sign}")


def format_month_total(
    *,
    amount: Decimal,
    currency: Currency,
    text: str = "Итого за месяц",
    max_name_len: int = 17,
    max_amount_len: int = 10,
) -> str:
    sign = currency_sign(currency)

    return monospace(f"{text:<{max_name_len}} | {amount:>{max_amount_len},.2f}{sign}")
