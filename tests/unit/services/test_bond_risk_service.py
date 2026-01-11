from unittest import mock

import pytest

from t_ledger.application.services.bond.risk import BondRiskServiceImpl
from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.models.core import Position, TotalAmountByInstrument, Portfolio, Bond
from t_ledger.domain.models.value_objects import Money, Quantity
from t_ledger.infra.api.consts import INSTRUMENT_TYPES


@pytest.fixture
def position_uids_with_types() -> list[tuple[str, str]]:
    return [
        ("01", "bond"), ("02", "futures"), ("03", "option"), ("04", "share"),
        ("05", "bond"), ("06", "futures"), ("07", "option"), ("08", "share"),
        ("09", "bond"), ("10", "futures"), ("11", "option"), ("12", "share"),
        ("13", "bond"), ("14", "futures"), ("15", "option"), ("16", "share"),
    ]


@pytest.fixture
def portfolio_instruments() -> set[str]:
    return {
        "totalAmountBonds", "totalAmountCurrencies", "totalAmountEtf",
        "totalAmountFutures", "totalAmountOptions", "totalAmountShares",
        "totalAmountSp",
    }


@pytest.fixture
def portfolio(position_uids_with_types, portfolio_instruments) -> Portfolio:
    positions = [
        Position(
            position_uid="...",
            instrument_uid=instr_uid,
            instrument_type=instr_type,
            current_price=Money.from_api({"nano": 0, "units": "10", "currency": "rub"}),
            quantity=Quantity.from_api({"nano": 0, "units": "10"}),
            daily_yield=Money.from_api({"nano": 0, "units": "1", "currency": "rub"}),
            current_nkd=Money.from_api({"nano": 0, "units": "0", "currency": "rub"}),
        )
        for instr_uid, instr_type in position_uids_with_types
    ]

    total_amounts_by_instrument = [
        TotalAmountByInstrument(
            instrument_type=enum_type,
            total_amount=Money.from_api({"nano": 0, "units": "40", "currency": "rub"}),
        )
        for json_field, enum_type in INSTRUMENT_TYPES.items()
        if json_field in portfolio_instruments
    ]

    return Portfolio(
        account_id="123",
        positions=positions,
        total_amount=Money.from_api({"nano": 0, "units": "160", "currency": "rub"}),
        daily_yield=Money.from_api({"nano": 0, "units": "16", "currency": "rub"}),
        total_amounts_by_instrument=total_amounts_by_instrument,
    )


@pytest.fixture
def bonds_data() -> dict[str, dict[str, str]]:
    return {
        "01": {
            "name": "ГК Самолет выпуск 13",
            "risk_level": "RISK_LEVEL_MODERATE",
        },
        "05": {
            "name": "ТГК-14 0001Р-05",
            "risk_level": "RISK_LEVEL_HIGH",
        },
        "09": {
            "name": "Кредитный поток 2.0",
            "risk_level": "RISK_LEVEL_LOW",
        },
        "13": {
            "name": "ОФЗ 26212",
            "risk_level": "RISK_LEVEL_LOW",
        },
    }


@pytest.fixture
def bonds(bonds_data) -> list[Bond]:
    return [
        Bond(
            instrument_uid=bond_uid,
            currency="rub",
            name=bond_data["name"],
            risk_level=bond_data["risk_level"],
            country_of_risk="RU",
        )
        for bond_uid, bond_data in bonds_data.items()
    ]


@pytest.fixture
def mock_api_client(portfolio, bonds):
    mock_client = mock.AsyncMock()

    mock_client.fetch_bonds.return_value = bonds
    mock_client.fetch_portfolio.return_value = portfolio

    return mock_client


@pytest.mark.asyncio
async def test_get_bonds_by_risks(mock_api_client, portfolio):
    service = BondRiskServiceImpl(mock_api_client)

    bonds_by_risks = await service.get_bonds_by_risks()

    # Разгруппировка облигаций в общий список
    bonds = []
    for bonds_by_risk in bonds_by_risks:
        bonds += bonds_by_risk.bonds

    # 1. Из общего списка инструментов отфильтрованы только облигации
    bond_position_uids = {
        position.instrument_uid
        for position in portfolio.positions
        if position.instrument_type == InstrumentType.BOND
    }

    assert all(map(lambda x: x.instrument_uid in bond_position_uids, bonds))

    # 2. Каждая облигация имеет поле `quantity`
    assert all(map(lambda x: x.quantity is not None, bonds))

    # 3. Облигации сгрупированы корректно
    for bonds_by_risk in bonds_by_risks:
        assert all(map(lambda x: x.risk_level == bonds_by_risk.risk_level, bonds_by_risk.bonds))
