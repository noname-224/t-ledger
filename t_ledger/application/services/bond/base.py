from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.models.core import Bond


class BondServiceMixin:
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def _build_bonds(self) -> list[Bond]:
        portfolio = await self._api_client.fetch_portfolio()

        bond_quantities = {
            position.instrument_uid: position.quantity
            for position in portfolio.positions
            if position.instrument_type == InstrumentType.BOND
        }

        bonds = await self._api_client.fetch_bonds(instrument_uids=list(bond_quantities))

        for bond in bonds:
            if bond.instrument_uid in bond_quantities:
                bond.quantity = bond_quantities[bond.instrument_uid]

        return bonds
