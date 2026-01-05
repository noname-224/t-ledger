import asyncio
from typing import Any

from aiohttp import ClientSession

from t_ledger.domain.exceptions import ApiClientRequestError
from t_ledger.infra.api.enums import Endpoint, Method
from t_ledger.infra.api.raw_models import RawAccount, RawPortfolio, RawPosition, RawBond, RawCoupon, \
    RawBondWithCoupons
from t_ledger.infra.api.consts import INSTRUMENT_TYPES, INSTRUMENT_ID_TYPE_UID, \
    COUPONS_BY_BONDS_END_DATE


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
            return RawAccount(id=data["accounts"][0]["id"])
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

        positions = [
            RawPosition(
                position_uid=position["positionUid"],
                instrument_uid=position["instrumentUid"],
                instrument_type=position["instrumentType"],
                current_price=position["currentPrice"],
                quantity=position["quantity"],
                daily_yield=position["dailyYield"],
                current_nkd=position.get("currentNkd"),
            )
            for position in data.get("positions", [])
        ]

        total_amounts_by_instrument = {
            key: data[key]
            for key in INSTRUMENT_TYPES
            if key in data
        }

        return RawPortfolio(
            account_id=data["accountId"],
            positions=positions,
            total_amount=data["totalAmountPortfolio"],
            daily_yield=data["dailyYield"],
            total_amounts_by_instrument=total_amounts_by_instrument,
        )

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

        result: list[RawBond] = []

        for uid, response in zip(bond_uids, responses):
            if isinstance(response, dict):
                instrument = response["instrument"]

                result.append(
                    RawBond(
                        instrument_uid=instrument["uid"],
                        currency=instrument["currency"],
                        name=instrument["name"],
                        risk_level=instrument["riskLevel"],
                        country_of_risk=instrument["countryOfRisk"],
                    ),
                )

        return result

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

        result: list[RawBondWithCoupons] = []

        for bond_uid, response in zip(bond_uids, responses):
            if isinstance(response, dict):
                coupons = [
                    RawCoupon(
                        coupon_date=event["couponDate"],
                        coupon_type=event["couponType"],
                        amount_per_bond=event["payOneBond"],
                    )
                    for event in response["events"]
                ]

                result.append(
                    RawBondWithCoupons(
                        instrument_uid=bond_uid,
                        coupons=coupons,
                    )
                )

        return result
