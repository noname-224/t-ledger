from typing import Any

from t_ledger.domain.exceptions import ApiClientError
from t_ledger.domain.models.core import (
    Account,
    Position,
    Portfolio,
    TotalAmountByInstrument,
    Bond,
    BondWithCouponSchedule,
    Coupon,
)
from t_ledger.domain.models.value_objects import Money, Quantity
from t_ledger.infra.api.consts import INSTRUMENT_TYPES


def account_from_api(response: dict[str, Any]) -> Account:
    try:
        return Account(id=response["accounts"][0]["id"])
    except (IndexError, KeyError, TypeError):
        raise ApiClientError("Error while parsing account")


def portfolio_from_api(response: dict[str, Any]) -> Portfolio:
    try:
        positions = [
            Position(
                position_uid=position["positionUid"],
                instrument_uid=position["instrumentUid"],
                instrument_type=position["instrumentType"],
                current_price=Money.from_api(position["currentPrice"]),
                quantity=Quantity.from_api(position["quantity"]),
                daily_yield=Money.from_api(position["dailyYield"]),
                current_nkd=Money.from_api(position.get("currentNkd")),
            )
            for position in response.get("positions", [])
        ]

        total_amounts_by_instrument = [
            TotalAmountByInstrument(
                instrument_type=enum_type,
                total_amount=Money.from_api(response[json_field]),
            )
            for json_field, enum_type in INSTRUMENT_TYPES.items()
            if json_field in response
        ]

        return Portfolio(
            account_id=response["accountId"],
            positions=positions,
            total_amount=Money.from_api(response["totalAmountPortfolio"]),
            daily_yield=Money.from_api(response["dailyYield"]),
            total_amounts_by_instrument=total_amounts_by_instrument,
        )
    except (AttributeError, KeyError, TypeError) as e:
        raise ApiClientError(f"Error while parsing portfolio {e}")


def bonds_from_api(
    responses: list[dict[str, Any] | BaseException], instrument_uids: list[str]
) -> list[Bond]:
    try:
        result: list[Bond] = []

        for uid, response in zip(instrument_uids, responses):
            if isinstance(response, BaseException):
                continue

            instrument = response["instrument"]

            result.append(
                Bond(
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


def bonds_with_coupons_from_api(
    responses: list[dict[str, Any] | BaseException],
    instrument_uids: list[str],
) -> list[BondWithCouponSchedule]:
    try:
        result: list[BondWithCouponSchedule] = []

        for uid, response in zip(instrument_uids, responses):
            if isinstance(response, BaseException):
                continue

            coupons = [
                Coupon(
                    coupon_date=event["couponDate"],
                    coupon_type=event["couponType"],
                    amount_per_bond=Money.from_api(event["payOneBond"]),
                )
                for event in response["events"]
            ]

            result.append(BondWithCouponSchedule(instrument_uid=uid, coupons=coupons))

        return result
    except (KeyError, TypeError):
        raise ApiClientError("Error while parsing bond coupons")
