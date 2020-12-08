from functools import wraps
from os import environ

import pytest
from fastapi.testclient import TestClient

from saatja.db.utils import configure_mock_db
from saatja.main import app

environ["LOGURU_FORMAT"] = "<lvl>{message}</lvl>"
configure_mock_db()


def reset_db(f):
    configure_mock_db()

    @wraps(f)
    def wrapper(*args, **kwargs):
        configure_mock_db()
        return f(*args, **kwargs)

    return wrapper


@pytest.fixture
def client():
    return TestClient(app)
