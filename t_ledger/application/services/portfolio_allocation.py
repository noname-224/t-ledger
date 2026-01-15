from decimal import Decimal

from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.interfaces.services import PortfolioAllocationService
from t_ledger.domain.models.core import PortfolioAllocation, PortfolioInstrumentAllocation
from t_ledger.domain.models.value_objects import Money


class PortfolioAllocationServiceImpl(PortfolioAllocationService):
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def get_portfolio_allocation(self) -> PortfolioAllocation:
        portfolio = await self._api_client.get_portfolio()

        daily_yield_by_instrument: dict[InstrumentType, Decimal] = {}

        # TODO а может быть такое что валюта инструмента не `RUB`
        for position in portfolio.positions:
            daily_yield_by_instrument[position.instrument_type] = (
                daily_yield_by_instrument.get(
                    position.instrument_type,
                    Decimal("0"),
                )
                + position.daily_yield.amount
            )

        instrument_allocations = sorted(
            (
                PortfolioInstrumentAllocation(
                    instrument_type=instrument_amount.instrument_type,
                    total_amount=instrument_amount.total_amount,
                    allocation_ratio=(
                        instrument_amount.total_amount.amount / portfolio.total_amount.amount
                    ),
                    daily_yield=Money(
                        amount=daily_yield_by_instrument[instrument_amount.instrument_type],
                        currency=instrument_amount.total_amount.currency,
                    ),
                )
                for instrument_amount in portfolio.total_amounts_by_instrument
                if instrument_amount.total_amount.is_positive
            ),
            key=lambda x: x.total_amount.amount,
            reverse=True,
        )

        return PortfolioAllocation(
            instrument_allocations=instrument_allocations,
            currency=portfolio.total_amount.currency,
        )
