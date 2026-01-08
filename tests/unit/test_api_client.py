import pytest

from t_ledger.domain.exceptions import ApiClientRequestError, ApiClientError
from t_ledger.infra.api.mappers.core import (
    parse_account,
    parse_portfolio,
    parse_bonds,
    parse_bonds_with_coupons,
)


@pytest.mark.asyncio
async def test_request_passed(api_client, mocked_request_params):
    data = await api_client._request(*mocked_request_params(status=200, json_data={"test": "test"}))

    assert data == {"test": "test"}


@pytest.mark.asyncio
async def test_request_failed(api_client, mocked_request_params):
    with pytest.raises(ApiClientRequestError):
        await api_client._request(*mocked_request_params(status=400, json_data={"test": "test"}))


def test_parse_account_passed(api_client):
    account_data = {
        "accounts": [
            {"id": "123"},
        ],
    }

    account = parse_account(account_data)

    assert account.id == account_data["accounts"][0]["id"]


@pytest.mark.parametrize(
    "account_data",
    [
        None,
        {},
        {"accounts": []},
        {"accounts": [{"test": "test"}]},
    ],
)
def test_parse_account_failed(api_client, account_data):
    with pytest.raises(ApiClientError):
        parse_account(account_data)


@pytest.mark.parametrize(
    "portfolio_data",
    [
        {
            "positions": [],
            "accountId": "123456789",
            "dailyYield": {"nano": 5, "currency": "currency", "units": "units"},
            "totalAmountPortfolio": {"nano": 5, "currency": "currency"},
            "totalAmountBonds": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountCurrencies": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountEtf": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountFutures": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountOptions": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountShares": {"nano": 5, "units": "units", "currency": "currency"},
            "totalAmountSp": {"nano": 5, "units": "units", "currency": "currency"},
        },
        {
            "accountId": "123456789",
            "dailyYield": {"nano": 5, "currency": "currency", "units": "units"},
            "totalAmountPortfolio": {"nano": 5, "currency": "currency"},
        },
    ],
)
def test_parse_portfolio_passed(api_client, portfolio_data):
    portfolio = parse_portfolio(portfolio_data)

    assert portfolio.account_id == portfolio_data["accountId"]


@pytest.mark.parametrize("portfolio_data", [{}, None])
def test_parse_portfolio_failed(api_client, portfolio_data):
    with pytest.raises(ApiClientError):
        parse_portfolio(portfolio_data)


def test_parse_bonds_passed():
    bonds_data = [
        {
            "instrument": {
                "countryOfRisk": "countryOfRisk",
                "name": "name",
                "uid": "uid",
                "currency": "currency",
                "riskLevel": "riskLevel",
            }
        },
        BaseException(),
    ]

    bonds_uids = ["uid", "uid"]

    bonds = parse_bonds(bonds_data, bonds_uids)

    assert len(bonds) != len(bonds_uids)


@pytest.mark.parametrize(
    "bonds_data,bonds_uids",
    [
        (
            [{"instrument": {}}],
            ["uid", "uid"],
        ),
        (
            [None],
            ["uid", "uid"],
        ),
    ],
)
def test_parse_bonds_failed(bonds_data, bonds_uids):
    with pytest.raises(ApiClientError):
        parse_bonds(bonds_data, bonds_uids)


def test_parse_bonds_with_coupons_passed():
    coupons_data = [
        {
            "events": [
                {
                    "couponType": "couponType",
                    "couponDate": "2000-01-23T04:56:07.000Z",
                    "payOneBond": {
                        "nano": 5,
                        "currency": "currency",
                        "units": "units",
                    },
                },
            ],
        },
        BaseException(),
    ]

    bonds_uids = ["uid", "uid"]

    bonds_with_coupons = parse_bonds_with_coupons(coupons_data, bonds_uids)

    assert bonds_with_coupons[0].instrument_uid == bonds_uids[0]


@pytest.mark.parametrize(
    "coupons_data,bonds_uids",
    [
        (
            [
                {
                    "events": [
                        {
                            "couponDate": "2000-01-23T04:56:07.000Z",
                            "payOneBond": {
                                "nano": 5,
                                "currency": "currency",
                                "units": "units",
                            },
                        },
                    ],
                },
                BaseException(),
            ],
            ["uid", "uid"],
        ),
        (
            None,
            ["uid", "uid"],
        ),
    ],
)
def test_parse_bonds_with_coupons_failed(coupons_data, bonds_uids):
    with pytest.raises(ApiClientError):
        parse_bonds_with_coupons(coupons_data, bonds_uids)
