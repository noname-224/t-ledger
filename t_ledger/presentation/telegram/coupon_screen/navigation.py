from t_ledger.domain.dtos import AnnualCouponIncome, MonthlyCouponIncome

from .models import YearMonth


class CouponNavigation:
    def __init__(self, data: list[AnnualCouponIncome]):
        self._months: list[YearMonth] = []
        self._data: dict[YearMonth, MonthlyCouponIncome] = {}

        for year_data in data:
            for month_data in year_data.months:
                ym = YearMonth(year=year_data.year, month=month_data.month)
                self._months.append(ym)
                self._data[ym] = month_data

        self._months.sort()

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

        idx = self._months.index(ym)
        if idx == 0:
            return None

        return self._months[idx - 1]

    def next(self, ym: YearMonth) -> YearMonth | None:
        if ym not in self._data:
            return None

        idx = self._months.index(ym)
        if idx == len(self._months) - 1:
            return None

        return self._months[idx + 1]