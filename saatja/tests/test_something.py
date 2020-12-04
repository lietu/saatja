from fastapi.testclient import TestClient

from saatja.api.models import CreateTask
from saatja.settings import conf
from saatja.utils import now_utc
from saatja.log import logger

AUTH_HEADERS = {"X-API-Key": next(iter(conf.API_KEYS))}


def test_anything(client: TestClient):
    payload = CreateTask(url="https://example.com/webhook", when=now_utc()).json()

    result = client.post("/task/", data=payload, headers=AUTH_HEADERS)

    if result.status_code != 201:
        logger.info("Create task failed: {content}", content=result.content)

    assert result.status_code == 201
