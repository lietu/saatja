import json
import sys
from os import environ
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request

from saatja.api.scheduler import scheduler_router
from saatja.api.tasks import task_router
from saatja.db.utils import configure_db
from saatja.log import logger
from saatja.settings import conf

OPENAPI_SPEC_FILE = "openapi/openapi.json"

app = FastAPI(title="Saatja webhook delivery system", version="1.0.0")
app.include_router(task_router, prefix="/task")
app.include_router(scheduler_router, prefix="/scheduler")
app.logger = logger


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "31536000"  # 1 year
    return response


@app.on_event("startup")
def initialize():
    configure_db()


def main():
    uvicorn.run(
        "saatja.main:app",
        host="0.0.0.0",  # nosec 0.0.0.0 is not a mistake
        port=conf.PORT,
        log_level="info",
    )


def dev():
    environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8686"
    main()


def openapi():
    from deepdiff import DeepDiff

    openapi_file = Path(OPENAPI_SPEC_FILE)
    openapi_spec = app.openapi()
    spec = json.dumps(openapi_spec, indent=2)

    content = spec.replace("\r\n", "\n").encode("utf-8")
    old_openapi_spec = json.loads(openapi_file.read_bytes())

    if DeepDiff(openapi_spec, old_openapi_spec, ignore_order=True) != {}:
        openapi_file.write_bytes(content)

        print(f"OpenAPI spec for Saatja written to {OPENAPI_SPEC_FILE}")
    else:
        print("OpenAPI spec does not require updates")


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "main":
        main()
    elif which == "openapi":
        openapi()
    else:
        raise Exception(f"No idea what {which} is.")
