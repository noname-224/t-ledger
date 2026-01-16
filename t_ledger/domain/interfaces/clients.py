from abc import ABC, abstractmethod

from t_ledger.domain.models.core import Bond, BondWithCouponSchedule, Portfolio


class TinkoffApiClient(ABC):
    @abstractmethod
    async def get_portfolio(self) -> Portfolio: ...

    @abstractmethod
    async def get_bonds(self) -> list[Bond]: ...

    @abstractmethod
    async def get_bonds_with_coupons(self) -> list[BondWithCouponSchedule]: ...
