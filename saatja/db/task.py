from datetime import datetime
from typing import Any

import aiohttp
from firedantic import Model

from saatja.log import logger
from saatja.utils import now_utc


class ScheduledTask(Model):
    __collection__ = "scheduled_tasks"

    url: str
    when: datetime
    payload: Any

    async def try_deliver(self) -> bool:
        """
        Try to deliver the webhook
        :return: If it was successful or not
        """
        safe_url = self._get_safe_url()
        logger.info(f"Trying to deliver webhook to {safe_url}")
        when = now_utc()
        try:
            response = await self._make_request()
            text = await response.text()
            if 200 <= response.status <= 299:
                # Success
                self._to_delivered_task(when, response.status, text)
                self.delete()
                logger.info(f"Successfully delivered webhook to {safe_url}")
                return True
            else:
                # Report error
                self._add_error(when, response.status, text)
                logger.error(
                    f"Got error {response.status} delivering webhook to {safe_url}"
                )
        except Exception as e:
            # Report error
            self._add_error(when, -1, str(e))
            logger.exception(
                f"Caught {type(e).__name__} delivering webhook to {safe_url}"
            )

        return False

    def _get_safe_url(self):
        """
        Try to get an URL without any authentication parameters etc. for logging purposes
        :return:
        """
        url = self.url
        if "?" in url:
            url = url.split("?", 2)[0]
        return url

    async def _make_request(self) -> aiohttp.ClientResponse:
        """This logic is annoyingly deep so made it into a function instead."""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=self.payload) as response:
                return response

    def _to_delivered_task(self, when: datetime, status: int, response: str):
        dt = DeliveredTask(
            **self.dict(),
            delivered=when,
            status=status,
            response=response,
        )

        dt.save()

    def _add_error(self, when: datetime, status: int, response: str):
        e = TaskError(
            task_id=self.id, attempted_delivery=when, status=status, response=response
        )

        e.save()


class DeliveredTask(Model):
    __collection__ = "delivered_tasks"

    url: str
    when: datetime
    delivered: datetime
    status: int
    response: str


class TaskError(Model):
    __collection__ = "task_errors"

    task_id: str
    attempted_delivery: datetime
    status: int
    response: str
