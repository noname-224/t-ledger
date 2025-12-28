from __future__ import annotations

from dataclasses import dataclass, replace


@dataclass(frozen=True, order=True)
class YearMonth:
    year: int
    month: int

    def shift_month(self, delta: int) -> YearMonth:
        total = self.year * 12 + (self.month - 1) + delta
        year = total // 12
        month = total % 12 + 1
        return replace(self, year=year, month=month)
