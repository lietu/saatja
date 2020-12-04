from datetime import datetime

from firedantic import Model
from pydantic import Field


class ScheduledTask(Model):
    __collection__ = "scheduled_tasks"

    url: str
    when: datetime

    async def try_deliver(self):
        pass

    def add_error(self, status, response, attempted_delivery):
        pass


class DeliveredTask(Model):
    __collection__ = "delivered_tasks"

    url: str
    when: datetime
    delivered: datetime
    status: int
    response: str


class TaskError(Model):
    __collection__ = "task_errors"

    task_id: str = Field(..., alias="taskId")
    attempted_delivery: datetime = Field(..., alias="attemptedDelivery")
    status: int
    response: str

    class Config:
        allow_population_by_field_name = True
