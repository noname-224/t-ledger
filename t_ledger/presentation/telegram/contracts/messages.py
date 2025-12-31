from enum import StrEnum


class BotMessageOption(StrEnum):
    TOTAL_AMOUNT_PORTFOLIO = "Общая стоимость портфеля"
    PORTFOLIO_ALLOCATION = "Аллокация портефеля"
    BOND_RISK_LEVELS = "Уровни риска облигаций"
    FUTURE_BOND_PAYMENTS = "Будущие выплаты по купонам"
