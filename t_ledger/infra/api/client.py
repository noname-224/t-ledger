import asyncio
from typing import Any

from aiohttp import ClientSession

from t_ledger.domain.exceptions import ApiClientRequestError
from t_ledger.infra.api.enums import Endpoint, Method
from t_ledger.infra.api.mappers.core import parse_portfolio, parse_bonds, parse_bonds_with_coupons, \
    parse_account
from t_ledger.infra.api.raw_models import RawAccount, RawPortfolio, RawBond, RawBondWithCoupons
from t_ledger.infra.api.consts import INSTRUMENT_ID_TYPE_UID, COUPONS_BY_BONDS_END_DATE


class TinkoffApiClient:
    def __init__(self, token: str, base_url: str) -> None:
        self._token = token
        self._base_url = base_url

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._token}"}

    async def _request(
        self,
        session: ClientSession,
        method: str,
        endpoint: str,
        json: dict | None = None,
    ) -> dict[str, Any]:
        async with session.request(
            method=method,
            url=self._base_url + endpoint,
            headers=self._headers(),
            ssl=False,
            json=json or {},
        ) as response:
            if response.status != 200:
                raise ApiClientRequestError(f"Code: {response.status}")

            return await response.json()

    async def _get_account(self, session: ClientSession) -> RawAccount | None:
        data = await self._request(
            session,
            method=Method.POST,
            endpoint=Endpoint.GET_ACCOUNTS,
            json={"status": "ACCOUNT_STATUS_ALL"}
        )

        try:
            return parse_account(data)
        except IndexError:
            return None

    async def get_portfolio_raw(self, session: ClientSession) -> RawPortfolio | None:
        account = await self._get_account(session)
        if account is None:
            return None

        data = await self._request(
            session,
            method=Method.POST,
            endpoint=Endpoint.GET_PORTFOLIO,
            json={"accountId": account.id, "currency": "RUB"}
        )

        return parse_portfolio(data)

    async def get_bonds_raw(
        self,
        session: ClientSession,
        *,
        bond_uids: list[str]
    ) -> list[RawBond]:
        tasks = [
            self._request(
                session,
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_BY,
                json={"idType": INSTRUMENT_ID_TYPE_UID, "id": uid}
            )
            for uid in bond_uids
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return parse_bonds(responses, bond_uids)

    async def get_bonds_with_coupons_raw(
        self,
        session: ClientSession,
        *,
        bond_uids: list[str],
    ) -> list[RawBondWithCoupons]:
        tasks = [
            self._request(
                session,
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_COUPONS,
                json={"instrumentId": uid, "to": COUPONS_BY_BONDS_END_DATE}
            )
            for uid in bond_uids
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        return parse_bonds_with_coupons(responses, bond_uids)
