from unittest.mock import AsyncMock

import pytest
from pytest_mock import MockerFixture


@pytest.fixture
def mocked_request_params(mocker: MockerFixture):
    def _factory(*, status: int, json_data: dict):
        session = mocker.Mock()

        response = mocker.Mock()
        response.status = status
        response.json = AsyncMock(return_value=json_data)

        context_manager = AsyncMock()
        context_manager.__aenter__.return_value = response
        context_manager.__aexit__.return_value = None

        session.request.return_value = context_manager

        return session, "", "", {}
    return _factory
