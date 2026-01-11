from decimal import Decimal

import pytest

from t_ledger.application.services.portfolio_allocation import PortfolioAllocationServiceImpl


@pytest.mark.asyncio
async def test_get_portfolio_allocation(mock_api_client):
    service = PortfolioAllocationServiceImpl(mock_api_client)

    portfolio_allocation = await service.get_portfolio_allocation()

    # 1. Список инструментов отсортирван в `DESC`
    # 2. Все типы инструментов в результате имеют общую сумму большую нуля
    for i in range(1, len(portfolio_allocation.instrument_allocations)):
        assert (
            portfolio_allocation.instrument_allocations[i - 1].total_amount.amount
            >= portfolio_allocation.instrument_allocations[i].total_amount.amount
        )
        assert portfolio_allocation.instrument_allocations[i].total_amount.amount > Decimal("0")
