from aiohttp import ClientSession

from t_ledger.domain.models.core import Position
from t_ledger.infra.api.enums import Endpoint, Method
from t_ledger.infra.api.raw_models import RawAccount, RawPortfolio, RawPosition, RawBond, RawCoupon
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
    ) -> dict:
        response = await session.request(
            method=method,
            url=self._base_url + endpoint,
            headers=self._headers(),
            ssl=False,
            json=json or {},
        )
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
        except (KeyError, IndexError):
            return None

    async def get_portfolio_raw(self) -> RawPortfolio | None:
        async with ClientSession() as session:
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
            for position in data["positions"]
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

    async def get_bonds_raw(self, bond_positions: list[Position]) -> list[RawBond]:
        async with ClientSession() as session:
            raw_bonds = []

            for position in bond_positions:
                data = (await self._request(
                    session,
                    method=Method.POST,
                    endpoint=Endpoint.GET_BOND_BY,
                    json={"idType": INSTRUMENT_ID_TYPE_UID, "id": position.instrument_uid}
                ))["instrument"]

                raw_bonds.append(
                    RawBond(
                        instrument_uid=data["uid"],
                        currency=data["currency"],
                        name=data["name"],
                        risk_level=data["riskLevel"],
                        country_of_risk=data["countryOfRisk"],
                    )
                )

        return raw_bonds

    async def get_coupons_by_bond_raw(self, bond_uid: str) -> list[RawCoupon]:
        async with ClientSession() as session:
            data = (await self._request(
                session,
                method=Method.POST,
                endpoint=Endpoint.GET_BOND_COUPONS,
                json={"instrumentId": bond_uid, "to": COUPONS_BY_BONDS_END_DATE}
            ))

        return [
            RawCoupon(
                coupon_date=event["couponDate"],
                coupon_type=event["couponType"],
                amount_per_bond=event["payOneBond"],
            )
            for event in data["events"]
        ]
