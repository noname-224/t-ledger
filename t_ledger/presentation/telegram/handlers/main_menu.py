from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from t_ledger.containers import Container
from t_ledger.domain.interfaces.services import (
    PortfolioService,
    PortfolioAllocationService,
    BondRiskService,
)
from t_ledger.presentation.telegram.contracts.commands import BotCommandOption
from t_ledger.presentation.telegram.contracts.messages import BotMessageOption
from t_ledger.presentation.telegram.presenters.portfolio import PortfolioPresenter


router = Router()


@router.message(F.text == BotMessageOption.TOTAL_AMOUNT_PORTFOLIO)
@router.message(Command(BotCommandOption.TOTAL_AMOUNT_PORTFOLIO))
@inject
async def handle_total_amount_portfolio(
    message: Message,
    portfolio_service: PortfolioService = Provide[Container.portfolio_service],
) -> None:
    portfolio = await portfolio_service.get_portfolio()
    text = await PortfolioPresenter.render_total_amount_portfolio(portfolio)

    await message.answer(text)


@router.message(F.text == BotMessageOption.PORTFOLIO_ALLOCATION)
@router.message(Command(BotCommandOption.PORTFOLIO_ALLOCATION))
@inject
async def handle_portfolio_allocation(
    message: Message,
    portfolio_allocation_service: PortfolioAllocationService = Provide[
        Container.portfolio_allocation_service
    ],
) -> None:
    portfolio_allocation = await portfolio_allocation_service.get_portfolio_allocation()
    text = await PortfolioPresenter.render_portfolio_allocation(portfolio_allocation)

    await message.answer(text)


@router.message(F.text == BotMessageOption.BONDS_BY_RISK)
@router.message(Command(BotCommandOption.BONDS_BY_RISK))
@inject
async def handle_bonds_by_risk(
    message: Message,
    bond_risk_service: BondRiskService = Provide[Container.bond_risk_service],
) -> None:
    bonds_by_risks = await bond_risk_service.get_bonds_by_risks()
    text = await PortfolioPresenter.render_bonds_grouped_by_risk_level(bonds_by_risks)

    await message.answer(text)
