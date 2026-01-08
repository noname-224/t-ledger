from typing import Any

from t_ledger.domain.exceptions import ApiClientError
from t_ledger.infra.api.consts import INSTRUMENT_TYPES
from t_ledger.infra.api.raw_models import (
    RawPosition,
    RawPortfolio,
    RawBond,
    RawBondWithCoupons,
    RawCoupon,
    RawAccount,
)


def parse_account(data: dict[str, Any]) -> RawAccount:
    try:
        return RawAccount(id=data["accounts"][0]["id"])
    except (IndexError, KeyError, TypeError):
        raise ApiClientError("Error while parsing account")


def parse_portfolio(data: dict[str, Any]) -> RawPortfolio:
    try:
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

        total_amounts_by_instrument = {key: data[key] for key in INSTRUMENT_TYPES if key in data}

        return RawPortfolio(
            account_id=data["accountId"],
            positions=positions,
            total_amount=data["totalAmountPortfolio"],
            daily_yield=data["dailyYield"],
            total_amounts_by_instrument=total_amounts_by_instrument,
        )
    except (AttributeError, KeyError, TypeError):
        raise ApiClientError("Error while parsing portfolio")


def parse_bonds(data: list[dict[str, Any] | BaseException], bond_uids: list[str]) -> list[RawBond]:
    try:
        result: list[RawBond] = []

        for uid, response in zip(bond_uids, data):
            if isinstance(response, BaseException):
                continue

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
    except (KeyError, TypeError):
        raise ApiClientError("Error while parsing bonds")


def parse_bonds_with_coupons(
    data: list[dict[str, Any] | BaseException],
    bond_uids: list[str],
) -> list[RawBondWithCoupons]:
    try:
        result: list[RawBondWithCoupons] = []

        for bond_uid, response in zip(bond_uids, data):
            if isinstance(response, BaseException):
                continue

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
    except (KeyError, TypeError):
        raise ApiClientError("Error while parsing bond coupons")
