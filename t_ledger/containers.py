from dependency_injector import containers, providers

from t_ledger.application.services.active_message import ActiveMessageServiceImpl
from t_ledger.application.services.bond.coupon import BondCouponServiseImpl
from t_ledger.application.services.bond.risk import BondRiskServiceImpl
from t_ledger.application.services.portfolio import PortfolioServiceImpl
from t_ledger.application.services.portfolio_allocation import PortfolioAllocationServiceImpl
from t_ledger.config import settings
from t_ledger.infra.api.client import TinkoffApiClientImpl
from t_ledger.infra.repositories import InMemoryMessageRepository


class Container(containers.DeclarativeContainer):
    tinkoff_api_client = providers.Singleton(
        TinkoffApiClientImpl,
        token=settings.tbank.token,
        base_url=settings.tbank.base_url,
    )

    message_repo = providers.Singleton(
        InMemoryMessageRepository,
    )

    portfolio_service = providers.Factory(
        PortfolioServiceImpl,
        api_client=tinkoff_api_client,
    )

    portfolio_allocation_service = providers.Factory(
        PortfolioAllocationServiceImpl,
        api_client=tinkoff_api_client,
    )

    bond_risk_service = providers.Factory(
        BondRiskServiceImpl,
        api_client=tinkoff_api_client,
    )

    bond_coupon_service = providers.Factory(
        BondCouponServiseImpl,
        api_client=tinkoff_api_client,
    )

    active_message_service = providers.Factory(
        ActiveMessageServiceImpl,
        message_repo=message_repo,
    )
