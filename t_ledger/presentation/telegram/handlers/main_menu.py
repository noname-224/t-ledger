from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from t_ledger.containers import Container
from t_ledger.presentation.telegram.contracts.commands import BotCommandOption
from t_ledger.presentation.telegram.contracts.messages import BotMessageOption
from t_ledger.presentation.telegram.presenters.portfolio import PortfolioPresenter


router = Router()

@router.message(F.text == BotMessageOption.TOTAL_AMOUNT_PORTFOLIO)
@router.message(Command(BotCommandOption.TOTAL_AMOUNT_PORTFOLIO))
@inject
async def handle_total_amount_portfolio(
    message: Message,
    portfolio_presenter: PortfolioPresenter = Provide[Container.portfolio_presenter],
) -> None:
    text = await portfolio_presenter.render_total_amount_portfolio()

    await message.answer(text)


@router.message(F.text == BotMessageOption.PORTFOLIO_ALLOCATION)
@router.message(Command(BotCommandOption.PORTFOLIO_ALLOCATION))
@inject
async def handle_portfolio_allocation(
    message: Message,
    portfolio_presenter: PortfolioPresenter = Provide[Container.portfolio_presenter],
) -> None:
    text = await portfolio_presenter.render_portfolio_allocation()

    await message.answer(text)


@router.message(F.text == BotMessageOption.BOND_RISK_LEVELS)
@router.message(Command(BotCommandOption.BOND_RISK_LEVELS))
@inject
async def handle_button(
    message: Message,
    portfolio_presenter: PortfolioPresenter = Provide[Container.portfolio_presenter],
) -> None:
    text = await portfolio_presenter.render_bonds_grouped_by_risk_level()

    await message.answer(text)
