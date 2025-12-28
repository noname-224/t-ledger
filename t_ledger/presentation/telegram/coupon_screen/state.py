from aiogram.fsm.state import StatesGroup, State


class CouponState(StatesGroup):
    browsing = State()
