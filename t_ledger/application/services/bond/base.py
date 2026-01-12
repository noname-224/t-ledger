from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.models.core import Bond


class BondServiceMixin:
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def _build_bonds(self) -> list[Bond]:
        portfolio = await self._api_client.get_portfolio()

        bond_quantities = {
            position.instrument_uid: position.quantity
            for position in portfolio.positions
            if position.instrument_type == InstrumentType.BOND
        }

        bonds = await self._api_client.get_bonds(instrument_uids=list(bond_quantities))

        for bond in bonds:
            bond.quantity = bond_quantities.get(bond.instrument_uid)

        return bonds
