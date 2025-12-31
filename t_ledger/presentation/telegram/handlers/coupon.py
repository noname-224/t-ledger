from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from dependency_injector.wiring import inject, Provide

from t_ledger.application.portfolio_service import PortfolioService
from t_ledger.containers import Container
from t_ledger.presentation.shared.models import YearMonth
from t_ledger.presentation.telegram.contracts.callbacks import CouponPagination
from t_ledger.presentation.telegram.contracts.commands import BotCommandOption
from t_ledger.presentation.telegram.contracts.messages import BotMessageOption
from t_ledger.presentation.telegram.presenters.coupon_calendar import CouponCalendarPresenter
from t_ledger.presentation.telegram.screens.coupon_calendar import CouponCalendarTimeline, \
    CouponCalendarState, build_coupon_keyboard
from t_ledger.presentation.telegram.texts.common import WINDOW_UNAVAILABLE, NO_COUPONS


router = Router()


@router.message(F.text == BotMessageOption.FUTURE_BOND_PAYMENTS)
@router.message(Command(BotCommandOption.FUTURE_BOND_PAYMENTS))
@inject
async def show_future_coupons(
    message: Message,
    state: FSMContext,
    portfolio_service: PortfolioService = Provide[Container.portfolio_service],
) -> None:
    data = await portfolio_service.get_future_payments_by_bonds()
    if not data:
        await message.answer(NO_COUPONS)
        return

    navigation = CouponCalendarTimeline(data)
    ym = navigation.first()

    await state.set_state(CouponCalendarState.browsing)
    await state.update_data(coupons=data)

    text = CouponCalendarPresenter().render_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    msg = await message.answer(text, reply_markup=keyboard)

    await state.update_data(active_msg_id=msg.message_id)


@router.callback_query(CouponPagination.filter(), CouponCalendarState.browsing)
async def paginate_coupons(
    callback: CallbackQuery,
    callback_data: CouponPagination,
    state: FSMContext
) -> None:
    data = await state.get_data()

    if callback.message.message_id != data["active_msg_id"]:
        await callback.answer(WINDOW_UNAVAILABLE, show_alert=True)
        return

    navigation = CouponCalendarTimeline(data["coupons"])
    ym = YearMonth(callback_data.year, callback_data.month)

    if not navigation.exists(ym):
        await callback.answer()
        return

    text = CouponCalendarPresenter().render_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    await callback.message.edit_text(text, reply_markup=keyboard)
