from http import HTTPStatus

from fastapi import Header, HTTPException

from saatja.settings import conf


def verified_api_key(x_api_key: str = Header(None)):
    """
    Require valid X-Api-Key header
    :param x_api_key:
    """
    if x_api_key not in conf.API_KEYS:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Invalid or missing API key")


def verified_scheduler(authorization: str = Header(None)):
    """
    Verify request is coming from Google Cloud Scheduler
    :param authorization:
    """

    # For easier unit test patching
    _check_scheduler_authorization(authorization)


def _check_scheduler_authorization(authorization: str):
    # TODO: Proper JWT verification
    if True:
        raise HTTPException(HTTPStatus.FORBIDDEN, "Access denied.")
