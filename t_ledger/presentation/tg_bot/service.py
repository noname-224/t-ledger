from aiogram import html

from t_ledger.application.service import InvestmentService
from t_ledger.domain.constants import currency_to_sign
from t_ledger.domain.enums import RiskLevel


class WindowLoaderService:
    service = InvestmentService()

    @classmethod
    async def load_portfolio_allocation_info(cls):
        alloc = await cls.service.get_portfolio_allocation()
        sign = currency_to_sign.get(alloc.currency.upper(), "¤")

        prepared_text = [
            (
                f"{html.bold(instr.type.upper())}\n"
                f"💰 Общая стоимость: {instr.total_amount.amount:.2f} {sign}\n"
                f"📊 % аллокации: {instr.alloc_percent:.2f}%\n"
                f"{"📈 Доход" if instr.daily_yield >= 0 else "📉 Убыток"}: {instr.daily_yield:.2f}"
                f" {sign}"
            )
            for instr in alloc.active_instruments
        ]

        return "\n\n".join(prepared_text)

    @classmethod
    async def load_bonds_risk_levels(cls):
        data = await cls.service.get_bonds()

        mapping = {
            RiskLevel.LOW: "🟢 Низкий уровень:",
            RiskLevel.MODERATE: "🟡 Средний уровень:",
            RiskLevel.HIGH: "🔴 Высокий уровень:",
            RiskLevel.UNSPECIFIED: "⚪️ Уровень риска не указан:",
        }

        prepared_text = []
        for risk_level, bonds in data.items():
            if bonds:
                prepared_text.append(f"{html.bold(mapping[risk_level])}")
                for bond in bonds:
                    prepared_text.append(f"    • {bond.name} ({bond.country_of_risk})")
                prepared_text.append("")

        return "\n".join(prepared_text)

    @classmethod
    async def load_total_amount_portfolio(cls):
        data = await cls.service.get_total_amount_portfolio()
        sign = currency_to_sign.get(data.total_amount_portfolio.currency.upper(), "¤")
        prepared_text = (
            f"💰 Общая стоимость: {data.total_amount_portfolio.amount:.2f} {sign}\n" 
            f"{"📈 Доход" if data.daily_yield.amount >= 0 
            else "📉 Убыток"}: {data.daily_yield.amount:.2f}"
        )
        return prepared_text