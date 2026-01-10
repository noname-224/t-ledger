from abc import ABC, abstractmethod
from typing import Any

from t_ledger.domain.enums.core import MessageType
from t_ledger.domain.models.core import (
    Portfolio,
    BondsByRiskLevel,
    AnnualCouponIncome,
    PortfolioAllocation,
)


class PortfolioService(ABC):
    @abstractmethod
    async def get_portfolio(self) -> Portfolio: ...


class PortfolioAllocationService(ABC):
    @abstractmethod
    async def get_portfolio_allocation(self) -> PortfolioAllocation: ...


class BondRiskService(ABC):
    @abstractmethod
    async def get_bonds_by_risk(self) -> list[BondsByRiskLevel]: ...


class BondCouponServise(ABC):
    @abstractmethod
    async def get_future_bond_payments(self) -> list[AnnualCouponIncome]: ...


class ActiveMessageService(ABC):
    @abstractmethod
    async def get_active_message(self, message_type: MessageType) -> tuple[int, Any] | None: ...

    @abstractmethod
    async def set_active_message(
        self, message_type: MessageType, message_id: int, message_data: Any
    ) -> None: ...
