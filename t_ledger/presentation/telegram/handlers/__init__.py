from aiogram import Dispatcher

from .coupon import router as coupon_calendar_router
from .main_menu import router as menu_router
from .start import router as start_router


def setup(dp: Dispatcher) -> None:
    dp.include_router(coupon_calendar_router)
    dp.include_router(menu_router)
    dp.include_router(start_router)
