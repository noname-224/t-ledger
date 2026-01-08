from t_ledger.application.portfolio_service import PortfolioService
from t_ledger.presentation.shared.formatting.portfolio import (
    format_alloc_block,
    format_risk_level_title,
    format_risk_level_block,
    format_total_amount_portfolio_text,
)


class PortfolioPresenter:
    def __init__(self, portfolio_service: PortfolioService):
        self._portfolio_service = portfolio_service

    async def render_total_amount_portfolio(self) -> str:
        data = await self._portfolio_service.get_portfolio()

        return format_total_amount_portfolio_text(
            currency=data.total_amount.currency,
            total_amount=data.total_amount.amount,
            daily_yield=data.daily_yield.amount,
        )

    async def render_portfolio_allocation(self) -> str:
        data = await self._portfolio_service.get_portfolio_allocation()
        lines = []

        for instrument in data.instrument_allocations:
            lines.append(
                format_alloc_block(
                    instr_type=instrument.instrument_type,
                    amount=instrument.total_amount.amount,
                    alloc_ratio=instrument.allocation_ratio,
                    daily_yield=instrument.daily_yield.amount,
                    currency=instrument.total_amount.currency,
                )
            )

        return "\n\n".join(lines)

    async def render_bonds_grouped_by_risk_level(self) -> str:
        data = await self._portfolio_service.get_bonds_grouped_by_risk_level()
        lines = []

        for bond_group in data:
            lines.append(format_risk_level_title(bond_group.risk_level))

            for bond in bond_group.bonds:
                lines.append(
                    format_risk_level_block(
                        bond_name=bond.name,
                        bond_country_of_risk=bond.country_of_risk,
                    )
                )

            lines.append("")

        return "\n".join(lines)
