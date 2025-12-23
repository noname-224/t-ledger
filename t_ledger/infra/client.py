from aiohttp import ClientSession

from t_ledger.config import settings
from t_ledger.constants import (
    Method,
    Currency,
    Endpoint,
    IdType,
)
from t_ledger.domain.entities import Position


class TinkoffApiClient:

    def __init__(self, token: str) -> None:
        self.__token = token

    def __get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.__token}"}

    async def __make_request(
        self,
        session: ClientSession,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        if headers is None:
            headers = self.__get_headers()

        if json is None:
            json = {}

        result = await session.request(
            method=method,
            url=settings.tbank.base_url + endpoint,
            headers=headers,
            ssl=False,
            json=json,
        )
        return await result.json(encoding="utf-8")

    async def __get_acc_id(self, session: ClientSession) -> str | None:
        result = await self.__make_request(
            session=session,
            method=Method.POST,
            endpoint=Endpoint.GET_ACCOUNTS,
            json={"status": "ACCOUNT_STATUS_ALL"},
        )
        try:
            return result["accounts"][0]["id"]
        except (KeyError, IndexError):
            return None

    async def get_portfolio_data(self) -> dict:
        async with ClientSession() as session:
            acc_id = await self.__get_acc_id(session)
            if acc_id is None:
                return None

            result = await self.__make_request(
                session=session,
                method=Method.POST,
                endpoint=Endpoint.GET_PORTFOLIO,
                json={"accountId": acc_id, "currency": Currency.RUB},  # TODO возможность передачи валюты?
            )
        return result

    async def get_risk_level(self,  positions: list[Position]) -> list:
        async with ClientSession() as session:
            result = [
                await self.__make_request(
                    session=session,
                    method=Method.POST,
                    endpoint=Endpoint.GET_BOND_BY,
                    json={"idType": IdType.UID, "id": position.instrument_uid}
                )
                for position in positions
            ]
        return result
