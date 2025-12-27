from aiogram import (
    Dispatcher,
    F,
)
from aiogram.filters import (
    CommandStart,
    Command,
)
from aiogram.types import Message

from t_ledger.presentation.tg_bot.constants import BotOption
from t_ledger.presentation.tg_bot.keyboards import main_keyboard
from t_ledger.presentation.tg_bot.middlewares import AccessMiddleware
from t_ledger.presentation.tg_bot.service import WindowLoaderService


dp = Dispatcher()
dp.message.outer_middleware(AccessMiddleware())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    text = (
        "Привет!😁\n"
        "Я могу предоставить информацию о твоем портфеле в Т-Инвестициях.\n\n"
        "Чтобы получить интересующую тебя информацию — выбери нужный пункт в меню, "
        "или отправь соответствующую команду."
    )
    await message.answer(text=text, reply_markup=main_keyboard())


@dp.message(F.text == BotOption.TOTAL_AMOUNT_PORTFOLIO)
@dp.message(Command("total_amount_portfolio"))
async def handle_button(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_total_amount_portfolio())


@dp.message(F.text == BotOption.PORTFOLIO_ALLOCATION)
@dp.message(Command("portfolio_allocation"))
async def handle(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_portfolio_allocation_info())


@dp.message(F.text == BotOption.BOND_RISK_LEVELS)
@dp.message(Command("bond_risk_levels"))
async def handle_button(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_bonds_risk_levels())
