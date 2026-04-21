from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from dependency_injector.wiring import Provide, inject

from t_ledger.containers import Container
from t_ledger.domain.enums.core import MessageType
from t_ledger.domain.interfaces.services import ActiveMessageService, BondCouponServise
from t_ledger.presentation.shared.models import YearMonth
from t_ledger.presentation.telegram.contracts.callbacks import CouponMonthCallback
from t_ledger.presentation.telegram.contracts.commands import BotCommandOption
from t_ledger.presentation.telegram.contracts.messages import BotMessageOption
from t_ledger.presentation.telegram.presenters.coupon_calendar import CouponCalendarPresenter
from t_ledger.presentation.telegram.screens.coupon_calendar import (
    CouponCalendarTimeline,
    build_coupon_keyboard,
)
from t_ledger.presentation.telegram.texts.common import WINDOW_UNAVAILABLE


router = Router()


@router.message(F.text == BotMessageOption.FUTURE_BOND_PAYMENTS)
@router.message(Command(BotCommandOption.FUTURE_BOND_PAYMENTS))
@inject
async def show_coupon_calendar(
    message: Message,
    bond_coupon_service: BondCouponServise = Provide[Container.bond_coupon_service],
    active_message_service: ActiveMessageService = Provide[Container.active_message_service],
) -> None:
    future_bond_payments = await bond_coupon_service.get_future_bond_payments()

    navigation = CouponCalendarTimeline(future_bond_payments)
    ym = navigation.first()

    text = CouponCalendarPresenter().render_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    msg = await message.answer(text, reply_markup=keyboard)

    await active_message_service.set_active_message(
        message_type=MessageType.FUTURE_BOND_PAYMENTS,
        message_id=msg.message_id,
        message_data=future_bond_payments,
    )


@router.callback_query(CouponMonthCallback.filter())
@inject
async def paginate_coupon_calendar(
    callback: CallbackQuery,
    callback_data: CouponMonthCallback,
    active_message_service: ActiveMessageService = Provide[Container.active_message_service],
) -> None:
    active_msg_data = await active_message_service.get_active_message(
        message_type=MessageType.FUTURE_BOND_PAYMENTS
    )

    active_msg_id, future_bond_payments = (
        active_msg_data if active_msg_data is not None else (None, None)
    )

    if active_msg_id is None or callback.message.message_id != active_msg_id:
        await callback.answer(WINDOW_UNAVAILABLE, show_alert=True)
        return

    navigation = CouponCalendarTimeline(future_bond_payments)
    ym = YearMonth(callback_data.year, callback_data.month)

    if not navigation.exists(ym):
        await callback.answer()
        return

    text = CouponCalendarPresenter().render_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    await callback.message.edit_text(text, reply_markup=keyboard)
