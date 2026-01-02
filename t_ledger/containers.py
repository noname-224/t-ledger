from dependency_injector import containers, providers

from t_ledger.application.portfolio_service import PortfolioService
from t_ledger.config import settings
from t_ledger.infra.repositories import InMemoryCouponRepository
from t_ledger.infra.api.client import TinkoffApiClient
from t_ledger.presentation.telegram.presenters.portfolio import PortfolioPresenter


class Container(containers.DeclarativeContainer):

    tinkoff_api_client = providers.Singleton(
        TinkoffApiClient,
        token=settings.tbank.token,
        base_url=settings.tbank.base_url,
    )

    portfolio_service = providers.Factory(
        PortfolioService,
        api_client=tinkoff_api_client,
    )

    portfolio_presenter = providers.Factory(
        PortfolioPresenter,
        portfolio_service=portfolio_service,
    )

    coupon_repository = providers.Singleton(
        InMemoryCouponRepository,
    )
