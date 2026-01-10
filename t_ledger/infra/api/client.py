import asyncio
from typing import Any

from aiohttp import ClientSession

from t_ledger.domain.exceptions import ApiClientRequestError
from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.models.core import Account, Portfolio, Bond, BondWithCouponSchedule
from t_ledger.infra.api.enums import Endpoint, Method
from t_ledger.infra.api.mappers.core import (
    portfolio_from_api,
    bonds_from_api,
    bonds_with_coupons_from_api,
    account_from_api,
)
from t_ledger.infra.api.consts import INSTRUMENT_ID_TYPE_UID, COUPONS_BY_BONDS_END_DATE


class TinkoffApiClientImpl(TinkoffApiClient):
    def __init__(self, token: str, base_url: str) -> None:
        self._token = token
        self._base_url = base_url
        self.__session: ClientSession | None = None

    async def fetch_portfolio(self) -> Portfolio:
        account = await self._fetch_account()

        response = await self._request(
            method=Method.POST,
            endpoint=Endpoint.GET_PORTFOLIO,
            json={"accountId": account.id, "currency": "RUB"},
        )

        return portfolio_from_api(response)

    async def fetch_bonds(self, instrument_uids: list[str]) -> list[Bond]:
        tasks = [
            self._request(
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_BY,
                json={"idType": INSTRUMENT_ID_TYPE_UID, "id": uid},
            )
            for uid in instrument_uids
        ]

        responses: list[dict[str, Any] | BaseException] = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        return bonds_from_api(responses, instrument_uids)

    async def fetch_bonds_with_coupons(
        self, instrument_uids: list[str]
    ) -> list[BondWithCouponSchedule]:
        tasks = [
            self._request(
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_COUPONS,
                json={"instrumentId": uid, "to": COUPONS_BY_BONDS_END_DATE},
            )
            for uid in instrument_uids
        ]

        responses: list[dict[str, Any] | BaseException] = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        return bonds_with_coupons_from_api(responses, instrument_uids)

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    @property
    def _session(self) -> ClientSession:
        if self.__session is None or self.__session.closed:
            self.__session = ClientSession()
        return self.__session

    async def _request(
        self,
        method: str,
        endpoint: str,
        json: dict | None = None,
    ) -> dict[str, Any]:
        async with self._session.request(
            method=method,
            url=self._base_url + endpoint,
            headers=self._headers(),
            ssl=False,
            json=json or {},
        ) as response:
            if response.status != 200:
                raise ApiClientRequestError(f"Code: {response.status}")

            return await response.json()

    async def _fetch_account(self) -> Account:
        data = await self._request(
            method=Method.POST,
            endpoint=Endpoint.GET_ACCOUNTS,
            json={"status": "ACCOUNT_STATUS_ALL"},
        )

        return account_from_api(data)
