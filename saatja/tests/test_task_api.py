from fastapi.testclient import TestClient

from saatja.api.models import CreateTask, CreateTaskResponse
from saatja.conftest import reset_db
from saatja.db.task import ScheduledTask
from saatja.settings import conf
from saatja.utils import now_utc

HEADERS = {"X-Api-Key": next(iter(conf.API_KEYS))}


@reset_db
def test_create_task(client: TestClient):
    payload = CreateTask(url="https://example.com", when=now_utc()).json()

    response = client.post("/task/", data=payload, headers=HEADERS)
    assert response.status_code == 201
    result = CreateTaskResponse(**response.json())
    assert result.id

    task = ScheduledTask.get_by_id(result.id)
    assert task.url == "https://example.com"
