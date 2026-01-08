from decimal import Decimal

from aiohttp import ClientSession

from t_ledger.application.utils import now
from t_ledger.domain.enums.core import RiskLevel
from t_ledger.domain.enums.currency import Currency
from t_ledger.domain.enums.instrument import InstrumentType
from t_ledger.domain.models.core import (
    Portfolio,
    TotalAmountByInstrument,
    PortfolioAllocation,
    PortfolioInstrumentAllocation,
    Position,
    Bond,
    BondsByRiskLevel,
    AnnualCouponIncome,
    Coupon,
    BondWithCouponSchedule,
    MonthlyCouponIncome,
)
from t_ledger.domain.models.value_objects import Money, Quantity
from t_ledger.infra.api.client import TinkoffApiClient


class PortfolioService:
    def __init__(self, api_client: TinkoffApiClient) -> None:
        self._api_client = api_client

    async def get_portfolio(self) -> Portfolio | None:
        async with ClientSession() as session:
            raw_portfolio = await self._api_client.get_portfolio_raw(session)
        if raw_portfolio is None:
            return None

        positions = [
            Position(
                position_uid=position.position_uid,
                instrument_uid=position.instrument_uid,
                instrument_type=InstrumentType.from_api(position.instrument_type),
                current_price=Money.from_api(position.current_price),
                quantity=Quantity.from_api(position.quantity),
                daily_yield=Money.from_api(position.daily_yield),
                current_nkd=(
                    Money.from_api(position.current_nkd)
                    if position.current_nkd is not None
                    else None
                ),
            )
            for position in raw_portfolio.positions
        ]

        prepared_total_amounts_by_instrument = {
            InstrumentType.from_api(instrument_type): Money.from_api(total_amount)
            for instrument_type, total_amount in raw_portfolio.total_amounts_by_instrument.items()
        }

        total_amounts_by_active_instrument = sorted(
            (
                TotalAmountByInstrument(
                    instrument_type=instrument_type,
                    total_amount=money,
                )
                for instrument_type, money in prepared_total_amounts_by_instrument.items()
                if money.is_positive
            ),
            key=lambda x: x.total_amount.amount,
            reverse=True,
        )

        return Portfolio(
            account_id=raw_portfolio.account_id,
            positions=positions,
            total_amount=Money.from_api(raw_portfolio.total_amount),
            daily_yield=Money.from_api(raw_portfolio.daily_yield),
            total_amounts_by_active_instrument=total_amounts_by_active_instrument,
        )

    async def get_portfolio_allocation(self) -> PortfolioAllocation | None:
        portfolio = await self.get_portfolio()
        if portfolio is None:
            return None

        daily_yield_by_instrument: dict[InstrumentType, Decimal] = {}

        for position in portfolio.positions:
            daily_yield_by_instrument[position.instrument_type] = (
                daily_yield_by_instrument.get(position.instrument_type, Decimal("0"))
                + position.daily_yield.amount
            )

        instrument_allocations = sorted(
            (
                PortfolioInstrumentAllocation(
                    instrument_type=instrument_amount.instrument_type,
                    total_amount=instrument_amount.total_amount,
                    allocation_ratio=(
                        instrument_amount.total_amount.amount / portfolio.total_amount.amount
                    ),
                    daily_yield=Money(
                        amount=daily_yield_by_instrument[instrument_amount.instrument_type],
                        currency=instrument_amount.total_amount.currency,
                    ),
                )
                for instrument_amount in portfolio.total_amounts_by_active_instrument
            ),
            key=lambda x: x.total_amount.amount,
            reverse=True,
        )

        return PortfolioAllocation(
            instrument_allocations=instrument_allocations,
            currency=portfolio.total_amount.currency,
        )

    async def _get_portfolio_bonds(self) -> list[Bond] | None:
        portfolio = await self.get_portfolio()
        if portfolio is None:
            return None

        bond_positions = list(
            filter(lambda x: x.instrument_type == InstrumentType.BOND, portfolio.positions)
        )

        bond_uids = [bond_position.instrument_uid for bond_position in bond_positions]

        async with ClientSession() as session:
            raw_bonds = await self._api_client.get_bonds_raw(session, bond_uids=bond_uids)

        raw_bonds_by_uid = {raw_bond.instrument_uid: raw_bond for raw_bond in raw_bonds}

        return [
            Bond(
                instrument_uid=raw_bonds_by_uid[position.instrument_uid].instrument_uid,
                currency=Currency.from_api(raw_bonds_by_uid[position.instrument_uid].currency),
                name=raw_bonds_by_uid[position.instrument_uid].name,
                country_of_risk=raw_bonds_by_uid[position.instrument_uid].country_of_risk,
                risk_level=raw_bonds_by_uid[position.instrument_uid].risk_level,
                quantity=position.quantity,
            )
            for position in bond_positions
            if position.instrument_uid in raw_bonds_by_uid
        ]

    async def get_bonds_grouped_by_risk_level(self) -> list[BondsByRiskLevel] | None:
        bonds = await self._get_portfolio_bonds()
        if bonds is None:
            return None

        bonds_by_risk_levels = {risk_level: [] for risk_level in RiskLevel}

        for bond in bonds:
            bonds_by_risk_levels[bond.risk_level].append(bond)

        return [
            BondsByRiskLevel(
                risk_level=risk_level,
                bonds=bonds,
            )
            for risk_level, bonds in bonds_by_risk_levels.items()
            if bonds
        ]

    async def _get_coupons_by_bonds(self, bonds: list[Bond]) -> list[BondWithCouponSchedule]:
        bond_uids = [bond.instrument_uid for bond in bonds]

        async with ClientSession() as session:
            raw_bonds_with_coupons = await self._api_client.get_bonds_with_coupons_raw(
                session,
                bond_uids=bond_uids,
            )

        raw_bonds_with_coupons_by_uid = {
            raw_bond_with_coupons.instrument_uid: raw_bond_with_coupons.coupons
            for raw_bond_with_coupons in raw_bonds_with_coupons
        }

        return [
            BondWithCouponSchedule(
                name=bond.name,
                quantity=bond.quantity,
                coupons=[
                    Coupon(
                        bond_name=bond.name,
                        quantity=bond.quantity,
                        coupon_date=raw_coupon.coupon_date,
                        coupon_type=raw_coupon.coupon_type,
                        amount_per_bond=Money.from_api(raw_coupon.amount_per_bond),
                    )
                    for raw_coupon in raw_bonds_with_coupons_by_uid[bond.instrument_uid]
                ],
            )
            for bond in bonds
            if bond.instrument_uid in raw_bonds_with_coupons_by_uid
        ]

    @staticmethod
    def _get_coupons_from_prev_payment(coupons: list[Coupon]) -> list[Coupon]:
        coupons_in_asc_by_date = list(reversed(coupons))
        left, right = 0, len(coupons_in_asc_by_date) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if coupons_in_asc_by_date[mid].coupon_date > now():
                right = mid - 1
            else:
                left = mid + 1

        return coupons_in_asc_by_date[left - 1 :]

    async def get_future_payments_by_bonds(self) -> list[AnnualCouponIncome]:
        bonds = await self._get_portfolio_bonds()
        if bonds is None:
            return None

        coupons_by_bonds = await self._get_coupons_by_bonds(bonds)

        coupons_by_year_month: dict[str, dict[str, list[Coupon]]] = {}

        for coupons_by_bond in coupons_by_bonds:
            required_period_coupons = self._get_coupons_from_prev_payment(coupons_by_bond.coupons)

            for i in range(1, len(required_period_coupons)):
                if required_period_coupons[i].amount_per_bond.amount == Decimal("0"):
                    pay_one_bond = required_period_coupons[i - 1].amount_per_bond
                    required_period_coupons[i].amount_per_bond = pay_one_bond

                coupons_by_year_month.setdefault(
                    required_period_coupons[i].coupon_date.year, {}
                ).setdefault(required_period_coupons[i].coupon_date.month, []).append(
                    required_period_coupons[i]
                )

        annual_incomes = []

        for year, months_data in coupons_by_year_month.items():
            monthly_incomes = []
            year_total = Decimal("0")

            for month, coupons in months_data.items():
                month_total = sum(
                    coupon.amount_per_bond.amount * coupon.quantity.value for coupon in coupons
                )

                monthly_incomes.append(
                    MonthlyCouponIncome(
                        month=month,
                        coupons=sorted(coupons, key=lambda x: x.coupon_date),
                        total_income=month_total,
                    )
                )

                year_total += month_total

            annual_incomes.append(
                AnnualCouponIncome(
                    year=year,
                    monthly_incomes=sorted(monthly_incomes, key=lambda x: x.month),
                    total_income=year_total,
                )
            )

        return annual_incomes
