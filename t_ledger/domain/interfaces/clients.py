from abc import ABC, abstractmethod

from t_ledger.domain.models.core import Portfolio, Bond, BondWithCouponSchedule


class TinkoffApiClient(ABC):
    @abstractmethod
    async def get_portfolio(self) -> Portfolio: ...

    @abstractmethod
    async def get_bonds(self) -> list[Bond]: ...

    @abstractmethod
    async def get_bonds_with_coupons(
        self, instrument_uids: list[str]
    ) -> list[BondWithCouponSchedule]: ...
