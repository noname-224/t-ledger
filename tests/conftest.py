import pytest

from t_ledger.config import settings
from t_ledger.infra.api.client import TinkoffApiClient


@pytest.fixture(scope="session")
def api_client():
    return TinkoffApiClient(
        token=settings.tbank.token,
        base_url=settings.tbank.base_url,
    )
