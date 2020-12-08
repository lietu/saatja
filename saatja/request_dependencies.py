from http import HTTPStatus

from fastapi import Header, HTTPException, Request

from saatja.settings import conf
from saatja.log import logger


def verified_api_key(x_api_key: str = Header(None)):
    """
    Require valid X-Api-Key header
    :param x_api_key:
    """
    if x_api_key not in conf.API_KEYS:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Invalid or missing API key")


def verified_scheduler(
    request: Request,
    user_agent: str = Header(None),
    x_cloudscheduler: str = Header(None),
):
    """
    Verify request is coming from Google Cloud Scheduler
    :param authorization:
    """

    logger.info("Verifying request. {headers}", headers=request.headers)

    # For easier unit test patching
    _check_scheduler_authorization(user_agent, x_cloudscheduler)


def _check_scheduler_authorization(user_agent: str, x_cloudscheduler: str):
    authed = True

    # TODO: Proper JWT verification, API key, or similar

    if user_agent != "Google-Cloud-Scheduler":
        authed = False

    if x_cloudscheduler != "true":
        authed = False

    if not authed:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access denied.")
