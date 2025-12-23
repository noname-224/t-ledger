from decimal import Decimal

from t_ledger.application.mappers import PortfolioMapper
from t_ledger.config import settings
from t_ledger.constants import InstrumentType
from t_ledger.domain.dtos import (
    PortfolioDTO,
    CategoryInfoDTO,
    BondInfoDTO,
)
from t_ledger.domain.entities import Portfolio
from t_ledger.infra.client import TinkoffApiClient


class SuperService:  # TODO я очень хочу подсказку
    api_client = TinkoffApiClient(settings.tbank.token)

    async def __get_portfolio_domain(self) -> Portfolio:
        data = await self.api_client.get_portfolio_data()
        return PortfolioMapper.to_domain(PortfolioDTO.model_validate(data))

    async def __get_risk_levels_dto(self, positions):
        data = await self.api_client.get_risk_level(positions)
        return [BondInfoDTO.model_validate(item) for item in data]

    async def get_portfolio_allocation(self) -> list[CategoryInfoDTO]:
        portfolio = await self.__get_portfolio_domain()

        categories_info = [
            CategoryInfoDTO(
                amount=category.amount.amount,
                category=category.category,
                currency=category.amount.currency,
                percentage=round(
                    category.amount.amount / portfolio.total_amount.amount * 100, 2
                ),
            )
            for category in portfolio.amounts_by_category
            if category.amount.amount > Decimal("0")
        ]

        return sorted(categories_info, key=lambda c: c.amount, reverse=True)

    async def get_positions_risk_levels(self) -> list[BondInfoDTO]:
        portfolio = await self.__get_portfolio_domain()

        bonds = [
            position
            for position in portfolio.positions
            if position.instrument_type == InstrumentType.BOND
        ]
        risk_levels = await self.__get_risk_levels_dto(bonds)

        return risk_levels
