from abc import ABC, abstractmethod

from t_ledger.domain.models.core import Portfolio, Bond, BondWithCouponSchedule


class TinkoffApiClient(ABC):
    @abstractmethod
    async def fetch_portfolio(self) -> Portfolio: ...

    @abstractmethod
    async def fetch_bonds(self, instrument_uids: list[str]) -> list[Bond]: ...

    @abstractmethod
    async def fetch_bonds_with_coupons(
        self, instrument_uids: list[str]
    ) -> list[BondWithCouponSchedule]: ...
