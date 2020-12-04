from fastapi import Header, HTTPException

from saatja.settings import conf


def verified_api_key(x_api_key: str = Header(None)):
    if x_api_key not in conf.API_KEYS:
        raise HTTPException(401, "Invalid or missing API key")


def verified_scheduler(authorization: str = Header(None)):
    pass  # TODO:
