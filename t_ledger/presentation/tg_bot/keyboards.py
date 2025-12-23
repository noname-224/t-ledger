from aiogram.utils.keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_window_buttons():
    """Keyboard for the welcome message"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Аллокация портефеля",
                    callback_data="get_portfolio_allocation",
                ),
                InlineKeyboardButton(
                    text="Уровни риска",
                    callback_data="get_risk_levels",
                ),
            ],
        ],
    )

def cancel_button():
    """"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data="cancel",
                ),
            ],
        ],
    )
