from aiogram import html

from t_ledger.application.service import SuperService


class WindowLoaderService:
    service = SuperService()

    @classmethod
    async def load_portfolio_allocation_info(cls):
        data = await cls.service.get_portfolio_allocation()
        text = [
            f"{i}. {d.category.capitalize()}: стоимость — {d.amount}, процент — {d.percentage}%"
            for i, d in enumerate(data, 1)
        ]

        return f"{html.bold("Аллокация портфеля:")}\n" + "\n".join(text)

    @classmethod
    async def load_bonds_risk_levels(cls):
        data = await cls.service.get_positions_risk_levels()
        text = [
            f"{i}. {d.name}: {d.risk_level_ru}"
            for i, d in enumerate(data, 1)
        ]

        return f"{html.bold("Уровни риска облигаций:")}\n" + "\n".join(text)
