from decimal import Decimal

import pytest

from t_ledger.application.services.bond.coupon import BondCouponServiseImpl
from t_ledger.domain.enums.core import Currency


@pytest.mark.asyncio
async def test_get_future_bond_payments(mock_api_client, mock_now):
    service = BondCouponServiseImpl(mock_api_client)

    future_bond_payments = await service.get_future_bond_payments()

    assert future_bond_payments

    # ASSERTS
    total_incomes = 0

    for year_data in future_bond_payments:
        total_incomes += year_data.total_income

        for month_data in year_data.monthly_incomes:
            for coupon in month_data.coupons:
                # 1. Все будущие выплаты имеют валюту и положительную сумму
                assert coupon.amount_per_bond.currency != Currency.NONE
                assert coupon.amount_per_bond.amount > Decimal("0")

                # 2. Все выплаты строго больше чем текущая дата "datetime(2026, 1, 25, tzinfo=UTC)"
                assert coupon.payment_date > mock_now

    # 3. Фактическая сумма всех будущих выплат равна ожидаемой
    assert total_incomes == Decimal("2194.8")
