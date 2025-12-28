from aiogram.filters.callback_data import CallbackData


class CouponPagination(CallbackData, prefix="coupon"):
    year: int
    month: int
