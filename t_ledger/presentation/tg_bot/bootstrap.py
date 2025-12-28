from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from t_ledger.config import settings
from t_ledger.presentation.tg_bot.handlers import dp


async def run_bot() -> None:
    bot = Bot(
        token=settings.tgbot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
