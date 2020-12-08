import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from firedantic import ModelNotFoundError

import saatja.request_dependencies as request_dependencies
from saatja.db.task import ScheduledTask, DeliveredTask, TaskError
from saatja.utils import now_utc

SCHEDULER_HEADERS = {"Authorization": "trustno1"}


class FakeResponse:
    def __init__(self, status: int, text: str):
        self.status = status
        self._text = text

    async def text(self):
        return self._text


def get_request_mock():
    requests = {
        "https://example.com/1": [
            FakeResponse(200, "Alles klar."),
        ],
        "https://example.com/2": [
            FakeResponse(500, "Oops."),
        ],
    }

    async def _mock_make_request(task: ScheduledTask):
        return requests[task.url].pop(0)

    return requests, _mock_make_request


def mock_check_authorization(authorization):
    if authorization != SCHEDULER_HEADERS["Authorization"]:
        raise HTTPException(403, "Access denied.")


def test_task_delivery(client: TestClient, monkeypatch):
    requests, request_mock = get_request_mock()
    monkeypatch.setattr(ScheduledTask, "_make_request", request_mock)
    monkeypatch.setattr(
        request_dependencies, "_check_scheduler_authorization", mock_check_authorization
    )

    task = ScheduledTask(url="https://example.com/1", when=now_utc())
    task.save()

    task2 = ScheduledTask(url="https://example.com/2", when=now_utc())
    task2.save()

    print("----- SCHEDULER TEST -----")
    print(f"Task 1: {task.id}")
    print(f"Task 2: {task2.id}")
    print("")

    response = client.post("/scheduler/run-tasks", headers=SCHEDULER_HEADERS)
    assert response.status_code == 204
    assert len(requests["https://example.com/1"]) == 0
    assert len(requests["https://example.com/2"]) == 0

    print("----- SCHEDULED TASKS -----")
    for r in ScheduledTask.find({}):
        print(f" - {r.id}: {r.when} -> {r.url}")
    print("")

    print("----- DELIVERED TASKS -----")
    for r in DeliveredTask.find({}):
        print(f" - {r.id}: {r.when} -> {r.url}")
    print("")

    print("----- TASK ERRORS -----")
    for r in TaskError.find({}):
        print(f" - {r.task_id}: {r.attempted_delivery} -> {r.status}")
    print("")

    # First task should've been delivered
    delivered = DeliveredTask.get_by_id(task.id)

    # These timestamps should be pretty close to each other
    assert abs((delivered.delivered - delivered.when).total_seconds()) < 2

    with pytest.raises(ModelNotFoundError):
        ScheduledTask.get_by_id(task.id)

    # Second task should've received an error
    ScheduledTask.get_by_id(task2.id)
    errors = TaskError.find({"task_id": task2.id})
    assert len(errors) == 1

    error: TaskError = errors[0]
    assert error.task_id == task2.id
    assert abs((error.attempted_delivery - task2.when).total_seconds()) < 2
    assert error.status == 500
    assert error.response == "Oops."
