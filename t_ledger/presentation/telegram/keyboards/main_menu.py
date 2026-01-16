from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from t_ledger.presentation.telegram.contracts.messages import BotMessageOption
from t_ledger.presentation.telegram.texts.common import INPUT_PLACE_HOLDER


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BotMessageOption.TOTAL_AMOUNT_PORTFOLIO)],
            [KeyboardButton(text=BotMessageOption.PORTFOLIO_ALLOCATION)],
            [KeyboardButton(text=BotMessageOption.BONDS_BY_RISK)],
            [KeyboardButton(text=BotMessageOption.FUTURE_BOND_PAYMENTS)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder=INPUT_PLACE_HOLDER,
    )
