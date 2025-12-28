from aiogram import (
    Dispatcher,
    F,
)
from aiogram.filters import (
    CommandStart,
    Command,
)
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from t_ledger.application.service import InvestmentService
from t_ledger.presentation.tg_bot.constants import (
    BotCommandOption,
    BotMessageOption,
    WINDOW_UNAVAILABLE_TEXT,
)
from t_ledger.presentation.tg_bot.coupon_screen import (
    CouponPagination,
    build_coupon_keyboard,
    YearMonth,
    CouponNavigation,
    CouponState,
    render_coupon_month,
)

from t_ledger.presentation.tg_bot.keyboards import main_keyboard
from t_ledger.presentation.tg_bot.middlewares import AccessMiddleware
from t_ledger.presentation.tg_bot.service import WindowLoaderService


dp = Dispatcher()
dp.message.outer_middleware(AccessMiddleware())


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """This handler receives messages with `/start` command"""
    text = (
        "Привет!😁\n"
        "Я могу предоставить информацию о твоем портфеле в Т-Инвестициях.\n\n"
        "Чтобы получить интересующую тебя информацию — выбери нужный пункт в меню, "
        "или отправь соответствующую команду."
    )
    await message.answer(text=text, reply_markup=main_keyboard())


@dp.message(F.text == BotMessageOption.TOTAL_AMOUNT_PORTFOLIO)
@dp.message(Command(BotCommandOption.TOTAL_AMOUNT_PORTFOLIO))
async def handle_button(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_total_amount_portfolio())


@dp.message(F.text == BotMessageOption.PORTFOLIO_ALLOCATION)
@dp.message(Command(BotCommandOption.PORTFOLIO_ALLOCATION))
async def handle(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_portfolio_allocation_info())


@dp.message(F.text == BotMessageOption.BOND_RISK_LEVELS)
@dp.message(Command(BotCommandOption.BOND_RISK_LEVELS))
async def handle_button(message: Message) -> None:
    await message.answer(
        await WindowLoaderService.load_bonds_risk_levels())


@dp.message(F.text == BotMessageOption.FUTURE_BOND_PAYMENTS)
@dp.message(Command(BotCommandOption.FUTURE_BOND_PAYMENTS))
async def show_future_coupons(message: Message, state: FSMContext) -> None:
    data = await InvestmentService().get_future_bond_payments()

    navigation = CouponNavigation(data)
    ym = navigation.first()

    await state.set_state(CouponState.browsing)
    await state.update_data(coupons=data)

    text = render_coupon_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    msg = await message.answer(text, reply_markup=keyboard)

    await state.update_data(active_msg_id=msg.message_id)


@dp.callback_query(CouponPagination.filter(), CouponState.browsing)
async def paginate_coupons(
    callback: CallbackQuery,
    callback_data: CouponPagination,
    state: FSMContext
) -> None:
    data = await state.get_data()

    if callback.message.message_id != data["active_msg_id"]:
        await callback.answer(WINDOW_UNAVAILABLE_TEXT, show_alert=True)
        return

    navigation = CouponNavigation(data["coupons"])
    ym = YearMonth(callback_data.year, callback_data.month)

    if not navigation.exists(ym):
        await callback.answer()
        return

    text = render_coupon_month(ym, navigation.get(ym))
    keyboard = build_coupon_keyboard(ym, navigation)

    await callback.message.edit_text(text, reply_markup=keyboard)
