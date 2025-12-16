import asyncio

from aiohttp import ClientSession

from config import settings
from constants import Method, BASE_URL


class TinkoffApiClient:

    def __init__(self, token: str) -> None:
        self.token = token


    def _get_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    async def _make_request(
        self,
        session: ClientSession,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> dict:
        if headers is None:
            headers = self._get_headers()

        if json is None:
            json = {}

        result = await session.request(
            method=method,
            url=BASE_URL + endpoint,
            headers=headers,
            ssl=False,
            json=json,
        )

        return await result.json(encoding="utf-8")

    async def _get_acc_id(self, session: ClientSession) -> str | None:
        result = await self._make_request(
            session=session,
            method=Method.POST,
            endpoint="/tinkoff.public.invest.api.contract.v1.UsersService/GetAccounts",
            json={"status": "ACCOUNT_STATUS_ALL"},
        )
        try:
            return result["accounts"][0]["id"]
        except IndexError:
            return None

    async def _get_portfolio(self, session: ClientSession) -> dict:
        acc_id = await self._get_acc_id(session)
        if acc_id is None:
            return None

        result = await self._make_request(
            session=session,
            method=Method.POST,
            endpoint="/tinkoff.public.invest.api.contract.v1.OperationsService/GetPortfolio",
            json={"accountId": acc_id, "currency": "RUB"},  # TODO возможность передачи валюты?
        )

        return result


    async def _get_portfolio_value(self, session: ClientSession) -> str | None:
        portfolio = await self._get_portfolio(session)
        if portfolio is None:
            return None

        units = int(portfolio["totalAmountPortfolio"]["units"])
        nano = round(portfolio["totalAmountPortfolio"]["nano"] / 1_000_000_000, 2)
        portfolio_value = str(units + nano)

        return portfolio_value

    async def get_portfolio_value(self) -> str | None:
        async with ClientSession() as session:
            portfolio_value = await self._get_portfolio_value(session)

        return portfolio_value

    async def get_portfolio_allocation(self) -> str:
        async with ClientSession() as session:
            portfolio_value = await self._get_portfolio_value(session)



class TinkoffDataService:

    def __init__(self):
        self.client: TinkoffApiClient = TinkoffApiClient("")



async def main():
    a = TinkoffApiClient(settings.tbank.token)

    result = await a.get_portfolio_value()
    print(result)

if __name__ == "__main__":
    asyncio.run(main())