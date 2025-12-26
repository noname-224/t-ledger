from aiogram import (
    Dispatcher,
    F,
)
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
)

from t_ledger.presentation.tg_bot.keyboards import (
    start_window_buttons,
    cancel_button,
)
from t_ledger.presentation.tg_bot.service import WindowLoaderService


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    await message.answer(text=f"Выберите действие.", reply_markup=start_window_buttons())


@dp.callback_query(F.data == "get_portfolio_allocation")
async def handle_button(call: CallbackQuery) -> None:
    await call.message.edit_text(
        await WindowLoaderService.load_portfolio_allocation_info(), reply_markup=cancel_button()
    )


@dp.callback_query(F.data == "get_risk_levels")
async def handle_button(call: CallbackQuery) -> None:
    await call.message.edit_text(
        await WindowLoaderService.load_bonds_risk_levels(), reply_markup=cancel_button()
    )


@dp.callback_query(F.data == "get_total_amount_portfolio")
async def handle_button(call: CallbackQuery) -> None:
    await call.message.edit_text(
        await WindowLoaderService.load_total_amount_portfolio(), reply_markup=cancel_button()
    )
