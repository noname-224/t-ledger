from enum import StrEnum


class BotMessageOption(StrEnum):
    TOTAL_AMOUNT_PORTFOLIO = "Общая стоимость портфеля"
    PORTFOLIO_ALLOCATION = "Аллокация портефеля"
    BONDS_BY_RISK = "Облигации по риску"
    FUTURE_BOND_PAYMENTS = "Будущие выплаты по купонам"
