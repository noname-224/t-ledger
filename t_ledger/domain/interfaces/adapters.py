from abc import ABC, abstractmethod
from typing import Any

from t_ledger.domain.models.core import (
    Account,
    Bond,
    BondWithCouponSchedule,
    Portfolio,
    PositionBond,
)


class AccountDTOAdapter(ABC):
    @abstractmethod
    def convert(self, response: dict[str, Any]) -> Account: ...


class PortfolioDTOAdapter(ABC):
    @abstractmethod
    def convert(self, response: dict[str, Any]) -> Portfolio: ...


class BondPositionsDTOAdapter(ABC):
    @abstractmethod
    def convert(self, response: dict[str, Any]) -> list[PositionBond]: ...


class BondsDTOAdapter(ABC):
    @abstractmethod
    def convert(
        self, responses: list[dict[str, Any] | Exception], bond_positions: list[PositionBond]
    ) -> list[Bond]: ...


class BondsWithCouponsDTOAdapter(ABC):
    @abstractmethod
    def convert(
        self, responses: list[dict[str, Any] | Exception], bonds: list[Bond]
    ) -> list[BondWithCouponSchedule]: ...
