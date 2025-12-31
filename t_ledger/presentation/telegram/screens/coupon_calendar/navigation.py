from t_ledger.domain.models.core import MonthlyCouponIncome, AnnualCouponIncome
from t_ledger.presentation.shared.models import YearMonth


class CouponCalendarTimeline:
    def __init__(self, data: list[AnnualCouponIncome]):
        self._months: list[YearMonth] = []
        self._indexes: dict[YearMonth, int] = {}
        self._data: dict[YearMonth, MonthlyCouponIncome] = {}

        for year_data in data:
            for month_data in year_data.monthly_incomes:
                ym = YearMonth(year=year_data.year, month=month_data.month)
                self._months.append(ym)
                self._data[ym] = month_data

        self._months.sort()
        self._indexes = {ym: idx for idx, ym in enumerate(self._months)}

    def first(self) -> YearMonth:
        return self._months[0]

    def last(self) -> YearMonth:
        return self._months[-1]

    def exists(self, ym: YearMonth) -> bool:
        return ym in self._data

    def get(self, ym: YearMonth) -> MonthlyCouponIncome | None:
        return self._data.get(ym)

    def prev(self, ym: YearMonth) -> YearMonth | None:
        if ym not in self._data:
            return None

        idx = self._indexes[ym]
        if idx == 0:
            return None

        return self._months[idx - 1]

    def next(self, ym: YearMonth) -> YearMonth | None:
        if ym not in self._data:
            return None

        idx = self._indexes[ym]
        if idx == len(self._months) - 1:
            return None

        return self._months[idx + 1]

    def shift(self, ym: YearMonth, delta: int) -> YearMonth | None:
        if ym not in self._indexes:
            return None

        idx = self._indexes[ym] + delta
        if 0 <= idx < len(self._months):
            return self._months[idx]
        return None
