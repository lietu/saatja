from datetime import datetime
from typing import Any

import aiohttp
from firedantic import Model

from saatja.log import logger
from saatja.utils import now_utc


class ScheduledTask(Model):
    __collection__ = "scheduledTasks"

    url: str
    when: datetime
    payload: Any

    async def try_deliver(self) -> bool:
        """
        Try to deliver the webhook
        :return: If it was successful or not
        """
        safe_url = self._get_safe_url()
        logger.info("Trying to deliver webhook to {safe_url}", safe_url=safe_url)
        when = now_utc()
        try:
            status, text = await self._make_request()
            if 200 <= status <= 299:
                # Success
                self._to_delivered_task(when, status, text)
                self.delete()
                logger.info(
                    "Successfully delivered webhook to {safe_url}", safe_url=safe_url
                )
                return True
            else:
                # Report error
                self._add_error(when, status, text)
                logger.error(
                    "Got error {status} delivering webhook to {safe_url}",
                    status=status,
                    safe_url=safe_url,
                )
        except Exception as e:
            # Report error
            self._add_error(when, -1, str(e))
            logger.exception(
                "Caught {t} delivering webhook to {safe_url}",
                t=type(e).__name__,
                safe_url=safe_url,
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

    async def _make_request(self) -> (int, str):
        """This logic is annoyingly deep so made it into a function instead."""
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=self.payload) as response:
                return response.status, await response.text()

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
    __collection__ = "deliveredTasks"

    url: str
    when: datetime
    delivered: datetime
    status: int
    response: str


class TaskError(Model):
    __collection__ = "taskErrors"

    task_id: str
    attempted_delivery: datetime
    status: int
    response: str
