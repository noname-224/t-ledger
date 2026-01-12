from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.models.core import Bond


class BondServiceMixin:
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def _build_bonds(self) -> list[Bond]:
        return await self._api_client.get_bonds()
