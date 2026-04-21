from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, order=True)
class YearMonth:
    year: int
    month: int
