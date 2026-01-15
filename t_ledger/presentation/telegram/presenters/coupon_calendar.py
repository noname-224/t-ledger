from t_ledger.domain.models.core import MonthlyCouponIncome
from t_ledger.presentation.shared.formatting.coupon_calendar import (
    format_coupon_line,
    format_month_title,
    format_month_total,
)
from t_ledger.presentation.shared.models import YearMonth


class CouponCalendarPresenter:
    def render_month(self, ym: YearMonth, month_data: MonthlyCouponIncome) -> str:
        lines = []  # noqa

        lines.append(self._render_header(ym))
        lines.append("")
        lines.extend(self._render_coupons(month_data))
        lines.append("")
        lines.append(self._render_total(month_data))

        return "\n".join(lines)

    def _render_header(self, ym: YearMonth) -> str:  # noqa
        return format_month_title(
            year=ym.year,
            month=ym.month,
        )

    def _render_coupons(self, month_data: MonthlyCouponIncome) -> list[str]:  # noqa
        lines = []

        for coupon in month_data.coupons:
            amount = coupon.amount_per_bond.amount * coupon.bond_quantity.value
            lines.append(
                format_coupon_line(
                    day=coupon.payment_date.day,
                    name=coupon.bond_name,
                    amount=amount,
                    currency=coupon.amount_per_bond.currency,
                )
            )

        return lines

    def _render_total(self, month_data: MonthlyCouponIncome) -> str:  # noqa
        return format_month_total(
            amount=month_data.total_income,
            currency=month_data.coupons[0].amount_per_bond.currency,
        )
