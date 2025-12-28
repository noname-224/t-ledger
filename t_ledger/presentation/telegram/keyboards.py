from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from t_ledger.presentation.tg_bot.constants import (
    BotMessageOption,
    PLACE_HOLDER,
)


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BotMessageOption.TOTAL_AMOUNT_PORTFOLIO)],
            [KeyboardButton(text=BotMessageOption.PORTFOLIO_ALLOCATION)],
            [KeyboardButton(text=BotMessageOption.BOND_RISK_LEVELS)],
            [KeyboardButton(text=BotMessageOption.FUTURE_BOND_PAYMENTS)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder=PLACE_HOLDER,
    )
