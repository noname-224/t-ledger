from aiogram import html

from t_ledger.domain.dtos import MonthlyCouponIncome, Coupon
from t_ledger.presentation.tg_bot.constants import MONTH_NAMES_RU, SUPERSCRIPTS, currency_to_sign
from t_ledger.presentation.utils import cut_line

from .models import YearMonth


def render_coupon_month(ym: YearMonth, month_data: MonthlyCouponIncome) -> str:
    lines: list[str] = [_render_hearder(ym)]
    max_name_len = 14
    sign = currency_to_sign.get(
        month_data.coupons[0].pay_one_bond.currency, "¤")


    total_income = f"{month_data.total_income:,.2f}"
    for coupon in month_data.coupons:
        lines.append(_render_coupon_line(
            coupon=coupon,
            max_amount_len=len(total_income),
            max_name_len=max_name_len,
        ))
    lines.append("")
    lines.append(f"<code>  </code>   "
                 f"<code>Итого за месяц</code> | <code>{total_income}</code> {sign}")
    return "\n".join(lines)


def _render_hearder(ym: YearMonth) -> str:
    year = "".join([SUPERSCRIPTS.get(digit) for digit in str(ym.year)])
    return f"{html.bold(MONTH_NAMES_RU.get(ym.month))}\n{year}"


def _render_coupon_line(
    coupon: Coupon,
    max_amount_len: int,
    max_name_len: int = 15,
) -> str:
    amount = coupon.pay_one_bond.amount * coupon.quantity.value
    amount_str = f"{amount:,.2f}"

    sign = currency_to_sign.get(
        coupon.pay_one_bond.currency, "¤")

    return (
        f"<code>{coupon.coupon_date.day:02d}</code> | "
        f"<code>{cut_line(coupon.bond_name, max_len=max_name_len).ljust(max_name_len)}</code> | "
        f"<code>{amount_str:>{max_amount_len}}</code> {sign}"
    )
