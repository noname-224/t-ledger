from datetime import UTC, datetime
from decimal import Decimal

from t_ledger.domain.interfaces.clients import TinkoffApiClient
from t_ledger.domain.interfaces.services import BondCouponServise
from t_ledger.domain.models.core import (
    AnnualCouponIncome,
    Coupon,
    MonthlyCouponIncome,
)
from t_ledger.domain.models.value_objects import Money


class BondCouponServiseImpl(BondCouponServise):
    def __init__(self, api_client: TinkoffApiClient):
        self._api_client = api_client

    async def get_future_bond_payments(self) -> list[AnnualCouponIncome]:
        bonds = await self._api_client.get_bonds_with_coupons()
        if not bonds:
            return []

        now = self._now()
        all_future_coupons = []

        for bond in bonds:
            last_paid_coupon, future = self._get_last_paid_and_future_coupons(bond.coupons, now)
            normalized = self._normalize_coupon_payment_amounts(
                future, last_paid_coupon.amount_per_bond if last_paid_coupon else None
            )
            all_future_coupons.extend(normalized)

        grouped = self._group_coupons_by_year_month(all_future_coupons)
        return self._build_coupon_income_by_year(grouped)

    def _get_last_paid_and_future_coupons(  # noqa
        self, coupons: list[Coupon], now: datetime
    ) -> tuple[Coupon | None, list[Coupon]]:
        """
        Возвращает кортеж из последнего выплаченного купона (или None)
        и списка будущих купонов, отсортированных по дате выплаты.
        """
        if not coupons:
            return None, []

        sorted_coupons = sorted(coupons, key=lambda x: x.payment_date)

        last_paid_coupon = None
        future = []

        for coupon in sorted_coupons:
            if coupon.payment_date <= now:
                last_paid_coupon = coupon
            else:
                future.append(coupon)

        return last_paid_coupon, future

    def _normalize_coupon_payment_amounts(  # noqa
        self, coupons: list[Coupon], initial_amount: Money | None = None
    ) -> list[Coupon]:
        """
        Нормализует значения купонных выплат.
        Если amount_per_bond == 0, используется значение предыдущего купона.
        """
        if not coupons:
            return []

        normalized = []
        prev_amount = initial_amount

        for coupon in coupons:
            amount = coupon.amount_per_bond

            if amount.amount == Decimal("0") and prev_amount is not None:
                amount = prev_amount

            normalized.append(coupon.model_copy(update={"amount_per_bond": amount}))

            prev_amount = amount

        return normalized

    def _group_coupons_by_year_month(  # noqa
        self, coupons: list[Coupon]
    ) -> dict[int, dict[int, list[Coupon]]]:
        """Группирует купоны по году и месяцу выплаты."""
        result: dict[int, dict[int, list[Coupon]]] = {}

        for coupon in coupons:
            result.setdefault(
                coupon.payment_date.year,
                {},
            ).setdefault(
                coupon.payment_date.month,
                [],
            ).append(coupon)

        return result

    def _build_coupon_income_by_year(  # noqa
        self, coupons_by_year_month: dict[int, dict[int, list[Coupon]]]
    ) -> list[AnnualCouponIncome]:
        """
        Агрегирует купоны, сгруппированные по годам и месяцам,
        в список моделей AnnualCouponIncome.
        """
        yearly_coupon_incomes = []

        for year, months_data in coupons_by_year_month.items():
            monthly_incomes = []
            year_total_income = Decimal("0")

            for month, coupons in months_data.items():
                month_total_income = sum(
                    coupon.amount_per_bond.amount * coupon.bond_quantity.value for coupon in coupons
                )

                monthly_incomes.append(
                    MonthlyCouponIncome(
                        month=month,
                        coupons=sorted(coupons, key=lambda x: x.payment_date),
                        total_income=month_total_income,
                    )
                )

                year_total_income += month_total_income

            yearly_coupon_incomes.append(
                AnnualCouponIncome(
                    year=year,
                    monthly_incomes=sorted(monthly_incomes, key=lambda x: x.month),
                    total_income=year_total_income,
                )
            )

        return yearly_coupon_incomes

    def _now(self) -> datetime:  # noqa
        """Возвращает текущую дату с тайм-зоной."""
        return datetime.now(UTC)
