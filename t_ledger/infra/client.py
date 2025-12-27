import asyncio
from datetime import datetime, timezone, timedelta
from pprint import pprint
from typing import Any

from aiohttp import ClientSession

from t_ledger.config import settings
from t_ledger.domain.constants import instrument_types
from t_ledger.domain.dtos import (
    Bond,
    Instrument,
    Portfolio,
    Position, Coupon, BondWithCoupons,
)
from t_ledger.domain.enums import (
    Method,
    Currency,
    Endpoint,
    InstrumentIdType, CouponType,
)


class TinkoffApiClient:

    def __init__(self, token: str) -> None:
        self.__token = token

    def __get_headers(self) -> dict[str: str]:
        return {"Authorization": f"Bearer {self.__token}"}

    async def __make_request(
        self,
        session: ClientSession,
        method: str,
        endpoint: str,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> dict[str: Any]:
        if headers is None:
            headers = self.__get_headers()

        if json is None:
            json = {}

        result = await (await session.request(
            method=method,
            url=settings.tbank.base_url + endpoint,
            headers=headers,
            ssl=False,
            json=json,
        )).json(encoding="utf-8")
        return result

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

    async def get_portfolio(self, currency: Currency = Currency.RUB) -> Portfolio | None:
        async with ClientSession() as session:
            acc_id = await self.__get_acc_id(session)
            if acc_id is None:
                return None

            data = await self.__make_request(
                session=session,
                method=Method.POST,
                endpoint=Endpoint.GET_PORTFOLIO,
                json={"accountId": acc_id, "currency": currency.upper()},
            )

        instruments = [
            Instrument(
                type=enum_type,
                total_amount=data[json_field],
            )
            for json_field, enum_type in instrument_types.items()
        ]

        portfolio = Portfolio(
            account_id=data["accountId"],
            positions=data["positions"],
            total_amount_portfolio=data["totalAmountPortfolio"],
            daily_yield=data["dailyYield"],
            instruments=instruments,
        )
        return portfolio

    async def get_bonds(self, positions: list[Position]) -> list[Bond]:
        async with ClientSession() as session:
            data = [
                Bond.model_validate((await self.__make_request(
                    session=session,
                    method=Method.POST,
                    endpoint=Endpoint.GET_BOND_BY,
                    json={"idType": InstrumentIdType.UID, "id": position.instrument_uid},
                ))["instrument"])
                for position in positions
            ]
        return data

    async def get_bonds_coupons(self, bonds: list[Bond]) -> list[BondWithCoupons]:
        async with ClientSession() as session:
            # from_ = datetime.now(timezone.utc)
            # to_ = from_ + timedelta(days=366)

            bonds_coupons = []
            for bond in bonds:
                cur_coupons = (await self.__make_request(
                    session=session,
                    method=Method.POST,
                    endpoint=Endpoint.GET_BOND_COUPONS,
                    json={
                        "instrumentId": bond.uid,
                        "to": (datetime.now(timezone.utc) + timedelta(days=365)).isoformat(),
                    },
                ))["events"]

                bonds_coupons.append(
                    BondWithCoupons(
                        name=bond.name,
                        coupons=[Coupon(**coupon) for coupon in cur_coupons],
                    )
                )

        return bonds_coupons



if __name__ == "__main__":
    async def main():
        client = TinkoffApiClient(settings.tbank.token)
        portfolio = await client.get_portfolio()
        coupon = await client.get_bonds_coupons(portfolio.positions[0].instrument_uid)
        pprint(coupon)

    asyncio.run(main())
