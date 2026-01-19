from unittest import mock

import pytest

from t_ledger.infra.api.adapters.core import (
    BondPositionsFromTinkoffAPIDTOAdapter,
    BondsFromTinkoffAPIDTOAdapter,
    PortfolioFromTinkoffAPIDTOAdapter,
)


@pytest.fixture(scope="session")
def mock_raw_portfolio():
    return {
        "accountId": "test_account_001",
        # ===== DAILY YIELD =====
        "dailyYield": {"currency": "rub", "units": "30", "nano": 700000000},
        "dailyYieldRelative": {"units": "0", "nano": 0},
        # ===== EXPECTED YIELD =====
        "expectedYield": {"units": "0", "nano": 0},
        # ===== POSITIONS =====
        "positions": [
            # --- bonds ---
            {
                "positionUid": "pos_bond_fixed",
                "instrumentUid": "bond_uid_fixed",
                "instrumentType": "bond",
                "currentPrice": {"currency": "rub", "units": "1020", "nano": 500000000},
                "quantity": {"units": "10", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "3", "nano": 200000000},
            },
            {
                "positionUid": "pos_bond_floating",
                "instrumentUid": "bond_uid_floating",
                "instrumentType": "bond",
                "currentPrice": {"currency": "rub", "units": "995", "nano": 800000000},
                "quantity": {"units": "15", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "2", "nano": 500000000},
            },
            {
                "positionUid": "pos_bond_variable",
                "instrumentUid": "bond_uid_variable",
                "instrumentType": "bond",
                "currentPrice": {"currency": "rub", "units": "980", "nano": 300000000},
                "quantity": {"units": "20", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "-1", "nano": -800000000},
            },
            # --- share ---
            {
                "positionUid": "pos_share",
                "instrumentUid": "share_uid_ydex",
                "instrumentType": "share",
                "currentPrice": {"currency": "rub", "units": "4600", "nano": 0},
                "quantity": {"units": "3", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "25", "nano": 0},
            },
            # --- etf ---
            {
                "positionUid": "pos_etf_1",
                "instrumentUid": "etf_uid_tech",
                "instrumentType": "etf",
                "currentPrice": {"currency": "rub", "units": "150", "nano": 600000000},
                "quantity": {"units": "100", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "-4", "nano": -300000000},
            },
            {
                "positionUid": "pos_etf_2",
                "instrumentUid": "etf_uid_dividend",
                "instrumentType": "etf",
                "currentPrice": {"currency": "rub", "units": "98", "nano": 900000000},
                "quantity": {"units": "250", "nano": 0},
                "dailyYield": {"currency": "rub", "units": "6", "nano": 100000000},
            },
        ],
        # ===== TOTALS =====
        "totalAmountBonds": {"currency": "rub", "units": "44748", "nano": 0},
        "totalAmountShares": {"currency": "rub", "units": "13800", "nano": 0},
        "totalAmountEtf": {"currency": "rub", "units": "39785", "nano": 0},
        "totalAmountCurrencies": {"currency": "rub", "units": "0", "nano": 0},
        "totalAmountFutures": {"currency": "rub", "units": "0", "nano": 0},
        "totalAmountOptions": {"currency": "rub", "units": "0", "nano": 0},
        "totalAmountSp": {"currency": "rub", "units": "0", "nano": 0},
        "totalAmountPortfolio": {"currency": "rub", "units": "98333", "nano": 0},
        # ===== VIRTUAL =====
        "virtualPositions": [],
    }


@pytest.fixture(scope="session")
def mock_portfolio(mock_raw_portfolio):
    adapter = PortfolioFromTinkoffAPIDTOAdapter()
    return adapter.convert(mock_raw_portfolio)


@pytest.fixture(scope="session")
def mock_bond_positions(mock_raw_portfolio):
    adapter = BondPositionsFromTinkoffAPIDTOAdapter()
    return adapter.convert(mock_raw_portfolio)


@pytest.fixture(scope="session")
def mock_raw_bonds():
    return [
        {
            "instrument": {
                "uid": "bond_uid_fixed",
                "currency": "rub",
                "name": "TEST BOND FIXED 2028",
                "countryOfRisk": "RU",
                "riskLevel": "RISK_LEVEL_LOW",
            },
        },
        {
            "instrument": {
                "uid": "bond_uid_floating",
                "currency": "rub",
                "name": "TEST BOND FLOATING 2029",
                "countryOfRisk": "RU",
                "riskLevel": "RISK_LEVEL_MODERATE",
            }
        },
        {
            "instrument": {
                "uid": "bond_uid_variable",
                "currency": "rub",
                "name": "TEST BOND VARIABLE 2030",
                "countryOfRisk": "RU",
                "riskLevel": "RISK_LEVEL_HIGH",
            }
        },
    ]


@pytest.fixture(scope="session")
def mock_bonds(mock_raw_bonds, mock_bond_positions):
    adapter = BondsFromTinkoffAPIDTOAdapter()
    return adapter.convert(mock_raw_bonds, mock_bond_positions)


@pytest.fixture(scope="session")
def mock_api_client(mock_portfolio, mock_bonds):
    mock_client = mock.AsyncMock()

    mock_client.get_portfolio.return_value = mock_portfolio
    mock_client.get_bonds.return_value = mock_bonds

    return mock_client
