from os import environ

import pytest
from fastapi.testclient import TestClient

from saatja.db.utils import configure_mock_db
from saatja.main import app

environ["LOGURU_FORMAT"] = "<lvl>{message}</lvl>"
configure_mock_db()


@pytest.fixture
def client():
    return TestClient(app)
