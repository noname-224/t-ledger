from decimal import Decimal

from t_ledger.domain.enums.core import RiskLevel
from t_ledger.domain.enums.core import Currency, InstrumentType
from t_ledger.presentation.shared.formatting.ui import currency_sign, bold


def format_total_amount_portfolio_text(
    *,
    currency: Currency,
    total_amount: Decimal,
    daily_yield: Decimal,
) -> str:
    sign = currency_sign(currency)
    return (
        f"💰 Общая стоимость: {total_amount:,.2f} {sign}\n"
        f"{_format_daily_yield_label(daily_yield)} {daily_yield:,.2f} {sign}\n"
    )


def format_alloc_block(
    *,
    instr_type: InstrumentType,
    amount: Decimal,
    alloc_ratio: Decimal,
    daily_yield: Decimal,
    currency: Currency,
) -> str:
    instr_name = _instrument_name(instr_type)
    sign = currency_sign(currency)

    return (
        f"{bold(instr_name)}\n"
        f"💰 Общая стоимость: {amount:,.2f} {sign}\n"
        f"📊 % аллокации: {alloc_ratio * 100:.2f}%\n"
        f"{_format_daily_yield_label(daily_yield)}: {daily_yield:,.2f} {sign}"
    )


def format_risk_level_title(risk_level: RiskLevel) -> str:
    return bold(_risk_level_text(risk_level))


def format_risk_level_block(*, bond_name: str, bond_country_of_risk: str) -> str:
    return f"    • {bond_name} [{bond_country_of_risk}]"


def _format_daily_yield_label(amount: Decimal) -> str:
    return "📈 Дневной доход" if amount >= Decimal("0") else "📉 Дневной убыток"


def _risk_level_text(level: RiskLevel | str) -> str:
    return {
        RiskLevel.LOW: "🟢 Низкий уровень:",
        RiskLevel.MODERATE: "🟡 Средний уровень:",
        RiskLevel.HIGH: "🔴 Высокий уровень:",
        RiskLevel.UNSPECIFIED: "⚪️ Уровень риска не указан:",
    }.get(level, "⚠️ Уровень риска не определен:")


def _instrument_name(instr_type: InstrumentType) -> str:
    return {
        InstrumentType.BOND: "ОБЛИГАЦИИ",
        InstrumentType.CURRENCY: "ВАЛЮТЫ",
        InstrumentType.ETF: "БИРЖЕВЫЕ ФОНДЫ",
        InstrumentType.FUTURES: "ФЬЮЧЕРСЫ",
        InstrumentType.OPTION: "ОПЦИОНЫ",
        InstrumentType.SHARE: "АКЦИИ",
        InstrumentType.SP: "СТРУКТУРНЫЕ ПРОДУКТЫ",
    }.get(instr_type, "...")
