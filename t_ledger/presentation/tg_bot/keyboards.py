from aiogram.utils.keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


def start_window_buttons():
    """Keyboard for the welcome message"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Аллокация портефеля",
                callback_data="get_portfolio_allocation",
            )],
            [InlineKeyboardButton(
                text="Уровни риска",
                callback_data="get_risk_levels",
            )],
            [InlineKeyboardButton(
                text="Стоимость портфеля",
                callback_data="get_total_amount_portfolio"
            )],
        ],
    )

def cancel_button():
    """"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Назад",
                callback_data="cancel",
            )],
        ],
    )
