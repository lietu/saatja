from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from saatja.api.models import (
    CreateTask,
    CreateTaskResponse,
    GetTaskResponse,
    GetTaskErrorResponse,
)
from saatja.db.task import ScheduledTask
from saatja.request_dependencies import verified_api_key

task_router = APIRouter()


@task_router.post(
    "/",
    summary="Create a task",
    description="Register a task to call a webhook at a given time",
    status_code=HTTPStatus.CREATED,
    response_model=CreateTaskResponse,
    dependencies=(Depends(verified_api_key),),
)
def create_task(data: CreateTask):
    task = ScheduledTask(**data.dict())
    task.save()

    return CreateTaskResponse(id=task.id)


@task_router.get(
    "/{task_id}",
    summary="Read a task",
    response_model=GetTaskResponse,
    description="NOT IMPLEMENTED. Check the status of the task based on the task ID received when creating the task",
    dependencies=(Depends(verified_api_key),),
)
def get_task(task_id: str):
    raise NotImplementedError()


@task_router.get(
    "/{task_id}/errors/{attempted_delivery}",
    summary="Explain error in webhook delivery attempt",
    response_model=GetTaskErrorResponse,
    description="NOT IMPLEMENTED. If reading a task shows errors, you can use this to check the specifics of the failure to help with debugging",
    dependencies=(Depends(verified_api_key),),
)
def get_task_error(task_id: str, attempted_delivery: str):
    raise NotImplementedError()


@task_router.delete(
    "/{task_id}",
    summary="Delete a task",
    status_code=HTTPStatus.NO_CONTENT,
    response_class=Response,
    description="NOT IMPLEMENTED. You can delete tasks before they are executed to abort or reschedule their delivery for another time",
    dependencies=(Depends(verified_api_key),),
)
def delete_task(task_id: str):
    raise NotImplementedError()
