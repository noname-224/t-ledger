from typing import Any

from t_ledger.domain.enums.core import InstrumentType
from t_ledger.domain.interfaces.adapters import (
    AccountDTOAdapter,
    BondPositionsDTOAdapter,
    BondsDTOAdapter,
    BondsWithCouponsDTOAdapter,
    PortfolioDTOAdapter,
)
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
from t_ledger.infra.api.adapters.mixins import (
    MoneyFieldDTOConverterMixin,
    QuantityFieldDTOConverterMixin,
)
from t_ledger.infra.api.consts import INSTRUMENT_TYPES


class AccountFromTinkoffAPIDTOAdapter(AccountDTOAdapter):
    def convert(self, response: dict[str, Any]) -> Account:
        return Account(id=response["accounts"][0]["id"])


class PortfolioFromTinkoffAPIDTOAdapter(
    MoneyFieldDTOConverterMixin, QuantityFieldDTOConverterMixin, PortfolioDTOAdapter
):
    def convert(self, response: dict[str, Any]) -> Portfolio:
        positions = [
            Position(
                position_uid=position["positionUid"],
                instrument_uid=position["instrumentUid"],
                instrument_type=position["instrumentType"],
                current_price=self._money_convert(position["currentPrice"]),
                quantity=self._quantity_convert(position["quantity"]),
                daily_yield=self._money_convert(position["dailyYield"]),
            )
            for position in response.get("positions", [])
        ]

        total_amounts_by_instrument = [
            TotalAmountByInstrument(
                instrument_type=enum_type,
                total_amount=self._money_convert(response[json_field]),
            )
            for json_field, enum_type in INSTRUMENT_TYPES.items()
            if json_field in response
        ]

        return Portfolio(
            account_id=response["accountId"],
            positions=positions,
            total_amount=self._money_convert(response["totalAmountPortfolio"]),
            daily_yield=self._money_convert(response["dailyYield"]),
            total_amounts_by_instrument=total_amounts_by_instrument,
        )


class BondPositionsFromTinkoffAPIDTOAdapter(
    QuantityFieldDTOConverterMixin, BondPositionsDTOAdapter
):
    def convert(self, response: dict[str, Any]) -> list[PositionBond]:
        return [
            PositionBond(
                instrument_uid=position["instrumentUid"],
                quantity=self._quantity_convert(position["quantity"]),
            )
            for position in response.get("positions", [])
            if position["instrumentType"] == InstrumentType.BOND
        ]


class BondsFromTinkoffAPIDTOAdapter(BondsDTOAdapter):
    def convert(
        self, responses: list[dict[str, Any] | Exception], bond_positions: list[PositionBond]
    ) -> list[Bond]:
        result: list[Bond] = []

        for position, response in zip(bond_positions, responses, strict=True):
            if isinstance(response, Exception):
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


class BondsWithCouponsFromTinkoffAPIDTOAdapter(
    MoneyFieldDTOConverterMixin, BondsWithCouponsDTOAdapter
):
    def convert(
        self, responses: list[dict[str, Any] | Exception], bonds: list[Bond]
    ) -> list[BondWithCouponSchedule]:
        result: list[BondWithCouponSchedule] = []

        for bond, response in zip(bonds, responses, strict=True):
            if isinstance(response, Exception):
                continue

            coupons = [
                Coupon(
                    payment_date=event["couponDate"],
                    coupon_type=event["couponType"],
                    amount_per_bond=self._money_convert(event["payOneBond"]),
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
