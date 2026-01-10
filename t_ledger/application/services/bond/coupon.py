from datetime import datetime, timezone
from decimal import Decimal

from t_ledger.application.services.bond.base import BondServiceMixin
from t_ledger.domain.interfaces.services import BondCouponServise
from t_ledger.domain.models.core import (
    AnnualCouponIncome,
    Coupon,
    Bond,
    BondWithCouponSchedule,
    MonthlyCouponIncome,
)


class BondCouponServiseImp(BondServiceMixin, BondCouponServise):
    async def get_future_bond_payments(self) -> list[AnnualCouponIncome]:
        return await self._build_future_bond_payment()

    async def _build_future_bond_payment(self) -> list[AnnualCouponIncome]:
        bonds = await self._build_bonds()

        coupons_by_bonds = await self._get_bonds_with_coupons(bonds)

        coupons_by_year_month: dict[str, dict[str, list[Coupon]]] = {}

        for coupons_by_bond in coupons_by_bonds:
            actual_coupons = self._get_coupons_from_prev_payment(coupons_by_bond.coupons)

            for i in range(1, len(actual_coupons)):
                if actual_coupons[i].amount_per_bond.amount == Decimal("0"):
                    actual_coupons[i].amount_per_bond = actual_coupons[i - 1].amount_per_bond

                coupons_by_year_month.setdefault(actual_coupons[i].coupon_date.year, {}).setdefault(
                    actual_coupons[i].coupon_date.month, []
                ).append(actual_coupons[i])

        annual_incomes = []

        for year, months_data in coupons_by_year_month.items():
            monthly_incomes = []
            year_total = Decimal("0")

            for month, coupons in months_data.items():
                month_total = sum(
                    coupon.amount_per_bond.amount * coupon.bond_quantity.value for coupon in coupons
                )

                monthly_incomes.append(
                    MonthlyCouponIncome(
                        month=month,
                        coupons=sorted(coupons, key=lambda x: x.coupon_date),
                        total_income=month_total,
                    )
                )

                year_total += month_total

            annual_incomes.append(
                AnnualCouponIncome(
                    year=year,
                    monthly_incomes=sorted(monthly_incomes, key=lambda x: x.month),
                    total_income=year_total,
                )
            )

        return annual_incomes

    async def _get_bonds_with_coupons(self, bonds: list[Bond]) -> list[BondWithCouponSchedule]:
        bond_data = {
            bond.instrument_uid: {
                "name": bond.name,
                "quantity": bond.quantity,
            }
            for bond in bonds
        }

        bonds_with_coupons = await self._api_client.fetch_bonds_with_coupons(list(bond_data))

        for bond in bonds_with_coupons:
            if bond.instrument_uid not in bond_data:
                continue

            bond.name = bond_data[bond.instrument_uid]["name"]
            bond.quantity = bond_data[bond.instrument_uid]["quantity"]

            for coupon in bond.coupons:
                coupon.bond_name = bond.name
                coupon.bond_quantity = bond.quantity

        return bonds_with_coupons

    @staticmethod
    def _get_coupons_from_prev_payment(coupons: list[Coupon]) -> list[Coupon]:
        """
        Функция отделения актуальных купонов облигации.

        Разворачивает исходный список купонов, для неубывающего порядка.
        Возвращает срез отсортированного списка купонов, начиная, со следующего,
        после крайнего выплаченного купона, заканчивая концом этого списка.
        Поиск начала среза происходит с помощью бинарного поиска.
        """

        coupons_in_asc_by_date = list(reversed(coupons))
        left, right = 0, len(coupons_in_asc_by_date) - 1

        while left <= right:
            mid = left + (right - left) // 2
            if coupons_in_asc_by_date[mid].coupon_date > datetime.now(timezone.utc):
                right = mid - 1
            else:
                left = mid + 1

        return coupons_in_asc_by_date[left - 1 :]
