from functools import partial

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callbacks import CouponPagination
from .models import YearMonth
from .navigation import CouponNavigation


def build_coupon_keyboard(
    ym: YearMonth,
    navigation: CouponNavigation,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    _build_month_switch_row(builder, ym, navigation)
    _build_quick_jump_row(builder, ym, navigation)

    return builder.as_markup()


def _build_month_switch_row(
    builder: InlineKeyboardBuilder,
    ym: YearMonth,
    navigation: CouponNavigation,
) -> None:
    row = []

    prev_ym = navigation.prev(ym)
    if prev_ym:
        row.append(_month_button("⬅️", prev_ym))

    next_ym = navigation.next(ym)
    if next_ym:
        row.append(_month_button("➡️", next_ym))

    if row:
        builder.row(*row)


def _build_quick_jump_row(
    builder: InlineKeyboardBuilder,
    ym: YearMonth,
    navigation: CouponNavigation,
) -> None:
    row = []

    back = _jump(navigation, ym, -3)
    if back:
        row.append(_month_button("⬅️ 3 мес.", back))

    forward = _jump(navigation, ym, 3)
    if forward:
        row.append(_month_button("3 мес. ➡️", forward))

    if row:
        builder.row(*row)


def _month_button(text: str, ym: YearMonth) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text=text,
        callback_data=CouponPagination(year=ym.year, month=ym.month).pack(),
    )


def _jump(
    navigation: CouponNavigation,
    ym: YearMonth,
    delta: int,
) -> YearMonth | None:
    current: YearMonth = ym

    move = partial(navigation.next) if delta > 0 else partial(navigation.prev)
    for _ in range(abs(delta)):
        current = move(current)
        if not current:
            return None

    return current
