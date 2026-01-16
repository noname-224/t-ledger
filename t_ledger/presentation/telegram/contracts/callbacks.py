from aiogram.filters.callback_data import CallbackData


class CouponMonthCallback(CallbackData, prefix="coupon"):
    year: int
    month: int
