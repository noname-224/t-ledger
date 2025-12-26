from aiogram.utils.keyboard import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)

from t_ledger.presentation.tg_bot.constants import BotOption


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BotOption.TOTAL_AMOUNT_PORTFOLIO)],
            [KeyboardButton(text=BotOption.PORTFOLIO_ALLOCATION)],
            [KeyboardButton(text=BotOption.BOND_RISK_LEVELS)],
        ],
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Выберите пункт меню.",
    )
