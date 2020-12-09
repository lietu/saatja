from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

import saatja.api.models
from saatja.api.models import CreateTask, CreateTaskResponse
from saatja.conftest import reset_db
from saatja.db.task import ScheduledTask
from saatja.log import logger
from saatja.settings import conf, Settings
from saatja.utils import now_utc

HEADERS = {"X-Api-Key": next(iter(conf.API_KEYS))}

TEST_SETTINGS = Settings()


@reset_db
def test_create_task(client: TestClient):
    payload = CreateTask(url="https://example.com", when=now_utc()).json()

    response = client.post("/task/", data=payload, headers=HEADERS)
    assert response.status_code == 201
    result = CreateTaskResponse(**response.json())
    assert result.id

    task = ScheduledTask.get_by_id(result.id)
    assert task.url == "https://example.com"


@reset_db
def test_validate_prefix(client: TestClient, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(saatja.api.models, "conf", TEST_SETTINGS)

    # HTTPS URLs should be allowed
    payload = CreateTask(url="https://example.com", when=now_utc()).json()
    response = client.post("/task/", data=payload, headers=HEADERS)

    logger.info(
        "Creating HTTPS task {code}: {response}",
        code=response.status_code,
        response=response.text,
    )
    assert response.status_code == 201

    # HTTP should not
    payload = payload.replace("https://", "http://")
    response = client.post("/task/", data=payload, headers=HEADERS)

    logger.info(
        "Creating HTTP task {code}: {response}",
        code=response.status_code,
        response=response.text,
    )
    assert response.status_code == 422
