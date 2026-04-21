import pytest

from t_ledger.application.services.bond.risk import BondRiskServiceImpl
from t_ledger.domain.enums.core import InstrumentType


@pytest.mark.asyncio
async def test_get_bonds_by_risks(mock_api_client, mock_portfolio):
    service = BondRiskServiceImpl(mock_api_client)

    bonds_by_risks = await service.get_bonds_by_risks()

    # Разгруппировка облигаций в общий список
    bonds = []
    for bonds_by_risk in bonds_by_risks:
        bonds += bonds_by_risk.bonds

    assert bonds

    # 1. Из общего списка инструментов отфильтрованы только облигации
    bond_position_uids = {
        position.instrument_uid
        for position in mock_portfolio.positions
        if position.instrument_type == InstrumentType.BOND
    }

    assert all(map(lambda x: x.instrument_uid in bond_position_uids, bonds))

    # 2. Облигации сгрупированы корректно
    for bonds_by_risk in bonds_by_risks:
        assert all(map(lambda x: x.risk_level == bonds_by_risk.risk_level, bonds_by_risk.bonds))
