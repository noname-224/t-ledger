from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from t_ledger.config import settings
from t_ledger.presentation.telegram.handlers import setup
from t_ledger.presentation.telegram.middlewares import AccessMiddleware


async def run_bot() -> None:
    bot = Bot(
        token=settings.tgbot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.message.outer_middleware(
        AccessMiddleware(settings.tgbot.allowed_user_ids)
    )
    setup(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
