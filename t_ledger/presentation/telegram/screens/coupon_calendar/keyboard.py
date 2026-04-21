from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from t_ledger.presentation.shared.models import YearMonth
from t_ledger.presentation.telegram.contracts.callbacks import CouponMonthCallback

from .navigation import CouponCalendarTimeline


def build_coupon_keyboard(
    ym: YearMonth,
    navigation: CouponCalendarTimeline,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    _build_month_switch_row(builder, ym, navigation)
    _build_quick_jump_row(builder, ym, navigation)

    return builder.as_markup()


def _build_month_switch_row(
    builder: InlineKeyboardBuilder,
    ym: YearMonth,
    navigation: CouponCalendarTimeline,
) -> None:
    row = []

    prev_ym = navigation.prev(ym)
    if prev_ym:
        row.append(_build_month_button("⬅️", prev_ym))

    next_ym = navigation.next(ym)
    if next_ym:
        row.append(_build_month_button("➡️", next_ym))

    if row:
        builder.row(*row)


def _build_quick_jump_row(
    builder: InlineKeyboardBuilder,
    ym: YearMonth,
    navigation: CouponCalendarTimeline,
) -> None:
    row = []

    back = navigation.shift(ym, -3)
    if back:
        row.append(_build_month_button("⬅️ 3 мес.", back))

    forward = navigation.shift(ym, 3)
    if forward:
        row.append(_build_month_button("3 мес. ➡️", forward))

    if row:
        builder.row(*row)


def _build_month_button(text: str, ym: YearMonth) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=CouponMonthCallback(year=ym.year, month=ym.month).pack(),
    )
