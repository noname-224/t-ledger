from enum import StrEnum


class BotMessageOption(StrEnum):
    TOTAL_AMOUNT_PORTFOLIO = "Общая стоимость портфеля"
    PORTFOLIO_ALLOCATION = "Аллокация портефеля"
    BOND_RISK_LEVELS = "Уровни риска облигаций"
    FUTURE_BOND_PAYMENTS = "Будущие выплаты по купонам"


class BotCommandOption(StrEnum):
    TOTAL_AMOUNT_PORTFOLIO = "total_amount_portfolio"
    PORTFOLIO_ALLOCATION = "portfolio_allocation"
    BOND_RISK_LEVELS = "bond_risk_levels"
    FUTURE_BOND_PAYMENTS = "future_bond_payments"


PLACE_HOLDER = "Выберите пункт меню."
WINDOW_UNAVAILABLE_TEXT = "Это окно не доступно."

currency_to_sign = {
    "eur": "€",
    "rub": "₽",
    "usd": "$",
}

MONTH_NAMES_RU = {
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

SUPERSCRIPTS = {
    "0": '⁰',
    "1": '¹',
    "2": '²',
    "3": '³',
    "4": '⁴',
    "5": '⁵',
    "6": '⁶',
    "7": '⁷',
    "8": '⁸',
    "9": '⁹',
}

