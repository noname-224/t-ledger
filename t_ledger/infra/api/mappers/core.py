from decimal import Decimal
from typing import Any

from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.exceptions import ApiClientError
from t_ledger.domain.models.core import (
    Account,
    Bond,
    BondWithCouponSchedule,
    Coupon,
    Portfolio,
    Position,
    PositionBond,
    TotalAmountByInstrument,
)
from t_ledger.domain.models.value_objects import Money, Quantity
from t_ledger.infra.api.consts import INSTRUMENT_TYPES


def portfolio_from_api(response: dict[str, Any]) -> Portfolio:
    try:
        positions = [
            Position(
                position_uid=position["positionUid"],
                instrument_uid=position["instrumentUid"],
                instrument_type=position["instrumentType"],
                current_price=_money_amount(position["currentPrice"]),
                quantity=_quantity_value(position["quantity"]),
                daily_yield=_money_amount(position["dailyYield"]),
            )
            for position in response.get("positions", [])
        ]

        total_amounts_by_instrument = [
            TotalAmountByInstrument(
                instrument_type=enum_type,
                total_amount=_money_amount(response[json_field]),
            )
            for json_field, enum_type in INSTRUMENT_TYPES.items()
            if json_field in response
        ]

        return Portfolio(
            account_id=response["accountId"],
            positions=positions,
            total_amount=_money_amount(response["totalAmountPortfolio"]),
            daily_yield=_money_amount(response["dailyYield"]),
            total_amounts_by_instrument=total_amounts_by_instrument,
        )
    except (AttributeError, KeyError, TypeError) as e:
        raise ApiClientError("Error while parsing portfolio.") from e


def bonds_from_api(
    responses: list[dict[str, Any] | BaseException],
    bond_positions: list[PositionBond],
) -> list[Bond]:
    try:
        result: list[Bond] = []

        for position, response in zip(bond_positions, responses, strict=True):
            if isinstance(response, BaseException):
                continue

            instrument = response["instrument"]

            result.append(
                Bond(
                    instrument_uid=instrument["uid"],
                    name=instrument["name"],
                    currency=instrument["currency"],
                    risk_level=instrument["riskLevel"],
                    country_of_risk=instrument["countryOfRisk"],
                    quantity=position.quantity,
                ),
            )

        return result
    except (KeyError, TypeError) as e:
        raise ApiClientError("Error while parsing bonds.") from e


def bonds_with_coupons_from_api(
    responses: list[dict[str, Any] | BaseException],
    bonds: list[Bond],
) -> list[BondWithCouponSchedule]:
    try:
        result: list[BondWithCouponSchedule] = []

        for bond, response in zip(bonds, responses, strict=True):
            if isinstance(response, BaseException):
                continue

            coupons = [
                Coupon(
                    coupon_date=event["couponDate"],
                    coupon_type=event["couponType"],
                    amount_per_bond=_money_amount(event["payOneBond"]),
                    bond_name=bond.name,
                    bond_quantity=bond.quantity,
                )
                for event in response["events"]
            ]

            result.append(
                BondWithCouponSchedule(
                    instrument_uid=bond.instrument_uid,
                    coupons=coupons,
                    name=bond.name,
                    quantity=bond.quantity,
                )
            )

        return result
    except (KeyError, TypeError) as e:
        raise ApiClientError("Error while parsing bond coupons.") from e


def bond_positions_from_api(response: dict[str, Any]) -> list[PositionBond]:
    return [
        PositionBond(
            instrument_uid=position["instrumentUid"],
            quantity=_quantity_value(position["quantity"]),
        )
        for position in response.get("positions", [])
        if position["instrumentType"] == InstrumentType.BOND
    ]


def account_from_api(response: dict[str, Any]) -> Account:
    try:
        return Account(id=response["accounts"][0]["id"])
    except (IndexError, KeyError, TypeError) as e:
        raise ApiClientError("Error while parsing account.") from e


def _money_amount(money_dict: dict[str, Any]) -> Money:
    return Money(
        amount=Decimal(money_dict["units"]) + Decimal(money_dict["nano"]) / Decimal("1e9"),
        currency=money_dict["currency"],
    )


def _quantity_value(quantity_dict: dict[str, Any]) -> Quantity:
    return Quantity(
        value=Decimal(quantity_dict["units"]) + Decimal(quantity_dict["nano"]) / Decimal("1e9")
    )
