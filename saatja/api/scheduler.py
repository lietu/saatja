import asyncio
from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from saatja.db.task import ScheduledTask
from saatja.log import logger
from saatja.request_dependencies import verified_scheduler
from saatja.utils import now_utc

scheduler_router = APIRouter()


@scheduler_router.post(
    "/run-tasks",
    summary="Run pending tasks",
    description="Fires off webhooks that are right now pending to be launched. Should be called every minute.",
    status_code=204,
    dependencies=(Depends(verified_scheduler),),
)
async def run_tasks():
    tasks = ScheduledTask.find({"when": {"<=": now_utc()}})
    logger.info("Found {count} tasks to run", count=len(tasks))
    await asyncio.gather(*[task.try_deliver() for task in tasks])
    return Response(status_code=HTTPStatus.NO_CONTENT)


@scheduler_router.post(
    "/maintenance",
    summary="Perform system maintenance",
    description="NOT IMPLEMENTED. Periodical maintenance tasks, database cleanup, etc. are performed here. Should likely be called about once a day.",
    dependencies=(Depends(verified_scheduler),),
)
def maintenance():
    raise NotImplementedError()
