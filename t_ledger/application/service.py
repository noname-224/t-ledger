import asyncio
import datetime
from decimal import Decimal
from pprint import pprint

from t_ledger.config import settings
from t_ledger.domain.dtos import (
    Allocation,
    Bond,
    InstrumentOut,
    Portfolio,
    Position, Coupon,
)
from t_ledger.domain.enums import (
    InstrumentType,
    RiskLevel, CouponType,
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

    async def get_future_bond_payments(self):
        portfolio = await self.api_client.get_portfolio()
        bond_positions = self.__get_bond_positions(portfolio)

        bond = await self.api_client.get_bonds(bond_positions)
        bonds_coupons = await self.api_client.get_bonds_coupons(bond)

        for bond_coupons in bonds_coupons:
            for coupon in bond_coupons.coupons:
                if coupon.coupon_date > datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30):
                    print(coupon)

if __name__ == "__main__":
    async def main():
        service = InvestmentService()
        await service.get_future_bond_payments()


    asyncio.run(main())
