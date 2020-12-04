from fastapi import APIRouter, Depends

from saatja.request_dependencies import verified_scheduler

scheduler_router = APIRouter()


@scheduler_router.post(
    "/run-tasks",
    summary="Run pending tasks",
    description="Fires off webhooks that are right now pending to be launched. Should be called every minute.",
    dependencies=(Depends(verified_scheduler),),
)
def run_tasks():
    pass


@scheduler_router.post(
    "/maintenance",
    summary="Perform system maintenance",
    description="Periodical maintenance tasks, database cleanup, etc. are performed here. Should likely be called about once a day.",
    dependencies=(Depends(verified_scheduler),),
)
def maintenance():
    raise NotImplementedError()
