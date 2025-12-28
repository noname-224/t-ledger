import datetime
from decimal import Decimal

from t_ledger.config import settings
from t_ledger.domain.dtos import (
    Allocation,
    AnnualCouponIncome,
    Bond,
    Coupon,
    InstrumentOut,
    MonthlyCouponIncome,
    Portfolio,
    Position,
)
from t_ledger.domain.enums import (
    InstrumentType,
    RiskLevel,
)
from t_ledger.infra.client import TinkoffApiClient


class InvestmentService:
    api_client = TinkoffApiClient(settings.tbank.token)

    @staticmethod
    def __get_bond_positions(portfolio: Portfolio) -> list[Position]:
        return [*filter(
            lambda x: x.instrument_type == InstrumentType.BOND,
            portfolio.positions,
        )]

    @staticmethod
    def __get_coupon_list_from_prev_payment(coupons: list[Coupon]) -> list[Coupon]:
        coupons_in_ascending_order = list(reversed(coupons))
        left, right = 0, len(coupons_in_ascending_order) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if coupons_in_ascending_order[mid].coupon_date > datetime.datetime.now(datetime.timezone.utc):
                right = mid - 1
            else:
                left = mid + 1

        return coupons_in_ascending_order[left - 1:]

    async def get_portfolio_allocation(self) -> Allocation:
        portfolio = await self.api_client.get_portfolio()

        daily_yield_by_types = {}
        for pos in portfolio.positions:
            daily_yield_by_types[pos.instrument_type] = (
                daily_yield_by_types.get(pos.instrument_type, Decimal("0")) +
                pos.daily_yield.amount
            )

        active_instruments = sorted(
            (
                InstrumentOut(
                    type=instr.type,
                    total_amount=instr.total_amount,
                    alloc_percent=(
                        instr.total_amount.amount / portfolio.total_amount_portfolio.amount * 100
                    ),
                    daily_yield=daily_yield_by_types[instr.type],
                )
                for instr in portfolio.instruments
                if instr.type in daily_yield_by_types
            ),
            key=lambda x: x.total_amount.amount,
            reverse=True,
        )

        allocation = Allocation(
            active_instruments=active_instruments,
            currency=portfolio.total_amount_portfolio.currency,
        )

        return allocation

    async def get_bonds(self) -> dict[RiskLevel: Bond]:
        portfolio = await self.api_client.get_portfolio()
        bond_positions = self.__get_bond_positions(portfolio)
        bonds = await self.api_client.get_bonds(bond_positions)

        bonds_by_risk_levels = {
            RiskLevel.LOW: [],
            RiskLevel.MODERATE: [],
            RiskLevel.HIGH: [],
            RiskLevel.UNSPECIFIED: [],
        }
        for bond in bonds:
            bonds_by_risk_levels[bond.risk_level] = bonds_by_risk_levels[bond.risk_level] + [bond]

        result = {
            risk_level: sorted(bonds, key=lambda x: x.name)
            for risk_level, bonds in bonds_by_risk_levels.items()
        }
        return result

    async def get_total_amount_portfolio(self) -> Portfolio:
        return await self.api_client.get_portfolio()

    async def get_future_bond_payments(self) -> list[AnnualCouponIncome]:
        portfolio = await self.api_client.get_portfolio()
        bond_positions = self.__get_bond_positions(portfolio)

        bonds = await self.api_client.get_bonds(bond_positions)
        bonds_coupons = await self.api_client.get_bonds_coupons(bonds)

        result: dict[str: dict[str: [Coupon]]] = {}
        for bond_coupons in bonds_coupons:

            coupons = self.__get_coupon_list_from_prev_payment(bond_coupons.coupons)
            for i in range(1, len(coupons)):

                if coupons[i].pay_one_bond.amount == Decimal("0"):
                    pay_one_bond = coupons[i - 1].pay_one_bond
                    coupons[i].pay_one_bond = pay_one_bond  # TODO !Изменение pydantic модели!
                result.setdefault(
                    coupons[i].coupon_date.year, {}).setdefault(
                    coupons[i].coupon_date.month, []).append(coupons[i])

        years = []
        for year, data in result.items():

            months, year_total = [], Decimal("0")
            for month, coupons in data.items():

                month_total = Decimal("0")
                for coupon in coupons:
                    month_total += coupon.pay_one_bond.amount * coupon.quantity.value

                months.append(MonthlyCouponIncome(
                    month=month,
                    coupons=sorted(coupons, key=lambda x: x.coupon_date),
                    total_income=month_total,
                ))
                year_total += month_total

            years.append(AnnualCouponIncome(
                year=year,
                months=sorted(months, key=lambda x: x.month),
                total_income=year_total,
            ))

        return sorted(years, key=lambda x: x.year)
