from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.interfaces.services import PortfolioService
from t_ledger.domain.models.core import Portfolio


class PortfolioServiceImpl(PortfolioService):
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def get_portfolio(self) -> Portfolio:
        return await self._api_client.get_portfolio()
