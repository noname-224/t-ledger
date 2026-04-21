from datetime import UTC, datetime
from unittest import mock

import pytest

from t_ledger.infra.api.adapters.core import (
    BondPositionsFromTinkoffAPIDTOAdapter,
    BondsFromTinkoffAPIDTOAdapter,
    BondsWithCouponsFromTinkoffAPIDTOAdapter,
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
def mock_raw_coupons():
    return [
        {
            # ===== TEST BOND FIXED 2028 (10 шт.)=====
            "events": [
                {
                    "couponDate": "2026-04-25T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2026-03-26T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2026-02-24T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                # --- купоны ниже уже выплачены и не идут в рассчет
                {
                    "couponDate": "2026-01-25T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2025-12-26T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2025-11-26T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2025-10-27T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2025-09-27T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
                {
                    "couponDate": "2025-08-28T00:00:00Z",
                    "couponType": "COUPON_TYPE_FIX",
                    "payOneBond": {"currency": "rub", "nano": 340000000, "units": "20"},
                },
            ]
        },
        # ===== TEST BOND FLOATING 2029 (15 шт.)=====
        {
            "events": [
                {
                    "couponDate": "2026-03-25T00:00:00Z",
                    "couponType": "COUPON_TYPE_FLOATING",
                    "payOneBond": {"currency": "", "nano": 0, "units": "0"},
                },
                # --- купоны ниже уже выплачены и не идут в рассчет
                {
                    "couponDate": "2025-12-24T00:00:00Z",
                    "couponType": "COUPON_TYPE_FLOATING",
                    "payOneBond": {"currency": "rub", "nano": 0, "units": "41"},
                },
                {
                    "couponDate": "2025-09-24T00:00:00Z",
                    "couponType": "COUPON_TYPE_FLOATING",
                    "payOneBond": {"currency": "rub", "nano": 90000000, "units": "46"},
                },
            ]
        },
        # ===== TEST BOND VARIABLE 2030 (20 шт.)=====
        {
            "events": [
                {
                    "couponDate": "2026-04-29T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "", "nano": 0, "units": "0"},
                },
                {
                    "couponDate": "2026-03-30T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "", "nano": 0, "units": "0"},
                },
                {
                    "couponDate": "2026-02-28T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "", "nano": 0, "units": "0"},
                },
                {
                    "couponDate": "2026-01-29T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                # --- купоны ниже уже выплачены и не идут в рассчет
                {
                    "couponDate": "2025-12-30T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                {
                    "couponDate": "2025-11-30T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                {
                    "couponDate": "2025-10-31T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                {
                    "couponDate": "2025-10-01T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                {
                    "couponDate": "2025-09-01T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
                {
                    "couponDate": "2025-08-02T00:00:00Z",
                    "couponType": "COUPON_TYPE_VARIABLE",
                    "payOneBond": {"currency": "rub", "nano": 120000000, "units": "12"},
                },
            ]
        },
    ]


@pytest.fixture(scope="session")
def mock_bonds_with_coupons(mock_raw_coupons, mock_bonds):
    adapter = BondsWithCouponsFromTinkoffAPIDTOAdapter()
    return adapter.convert(mock_raw_coupons, mock_bonds)


@pytest.fixture(scope="session")
def mock_api_client(mock_portfolio, mock_bonds, mock_bonds_with_coupons):
    mock_client = mock.AsyncMock()

    mock_client.get_portfolio.return_value = mock_portfolio
    mock_client.get_bonds.return_value = mock_bonds
    mock_client.get_bonds_with_coupons.return_value = mock_bonds_with_coupons

    return mock_client


@pytest.fixture
def mock_now(monkeypatch):
    from t_ledger.application.services.bond.coupon import BondCouponServiseImpl

    fixed_time = datetime(2026, 1, 25, tzinfo=UTC)

    monkeypatch.setattr(
        BondCouponServiseImpl,
        "_now",
        lambda self: fixed_time,
    )

    return fixed_time
