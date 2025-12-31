from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from t_ledger.presentation.telegram.keyboards.main_menu import main_menu_keyboard
from t_ledger.presentation.telegram.texts.common import GREETING


router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(GREETING, reply_markup=main_menu_keyboard())
