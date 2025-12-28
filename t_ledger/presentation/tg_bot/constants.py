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
