import asyncio
from typing import Any

from aiohttp import ClientSession

from t_ledger.domain.exceptions import ApiClientRequestError
from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.models.core import (
    Account,
    Bond,
    BondWithCouponSchedule,
    Portfolio,
    PositionBond,
)
from t_ledger.infra.api.consts import COUPONS_BY_BONDS_END_DATE, INSTRUMENT_ID_TYPE_UID
from t_ledger.infra.api.enums import Endpoint, Method
from t_ledger.infra.api.mappers.core import (
    account_from_api,
    bond_positions_from_api,
    bonds_from_api,
    bonds_with_coupons_from_api,
    portfolio_from_api,
)


class TinkoffApiClientImpl(TinkoffApiClient):
    def __init__(self, token: str, base_url: str) -> None:
        self._token = token
        self._base_url = base_url
        self.__session: ClientSession | None = None

    async def get_portfolio(self) -> Portfolio:
        portfolio = await self._fetch_portfolio()
        return portfolio_from_api(portfolio)

    async def get_bonds(self) -> list[Bond]:
        bond_positions = await self._get_bond_positions()

        tasks = [
            self._request(
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_BY,
                json={"idType": INSTRUMENT_ID_TYPE_UID, "id": position.instrument_uid},
            )
            for position in bond_positions
        ]

        responses: list[dict[str, Any] | BaseException] = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        return bonds_from_api(responses, bond_positions)

    async def get_bonds_with_coupons(self) -> list[BondWithCouponSchedule]:
        bonds = await self.get_bonds()

        tasks = [
            self._request(
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_COUPONS,
                json={"instrumentId": bond.instrument_uid, "to": COUPONS_BY_BONDS_END_DATE},
            )
            for bond in bonds
        ]

        responses: list[dict[str, Any] | BaseException] = await asyncio.gather(
            *tasks,
            return_exceptions=True,
        )

        return bonds_with_coupons_from_api(responses, bonds)

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

    async def _get_account(self) -> Account:
        data = await self._request(
            method=Method.POST,
            endpoint=Endpoint.GET_ACCOUNTS,
            json={"status": "ACCOUNT_STATUS_ALL"},
        )

        return account_from_api(data)

    async def _fetch_portfolio(self) -> Portfolio:
        account = await self._get_account()

        return await self._request(
            method=Method.POST,
            endpoint=Endpoint.GET_PORTFOLIO,
            json={"accountId": account.id, "currency": "RUB"},
        )

    async def _get_bond_positions(self) -> list[PositionBond]:
        portfolio = await self._fetch_portfolio()
        return bond_positions_from_api(portfolio)
