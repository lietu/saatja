import json
import sys
from os import environ
from pathlib import Path

import uvicorn
from uvicorn.supervisors import ChangeReload

from saatja.settings import conf

OPENAPI_SPEC_FILE = "openapi/openapi.json"


# Entrypoints for Poetry


def main(log_level="info"):
    server = uvicorn.Server(
        uvicorn.Config(
            app="saatja.app:app",
            host="0.0.0.0",  # nosec 0.0.0.0 is not a mistake
            port=conf.PORT,
            log_level=log_level,
            reload=False,
        ),
    )
    server.run()


def dev(log_level="debug"):
    environ["FIRESTORE_EMULATOR_HOST"] = "127.0.0.1:8686"
    config = uvicorn.Config(
        app="saatja.app:app",
        host="0.0.0.0",  # nosec 0.0.0.0 is not a mistake
        port=conf.PORT,
        log_level=log_level,
        reload=False,
    )
    server = uvicorn.Server(config)

    # Activate logging configuration
    from saatja.log import logger

    _ = logger

    supervisor = ChangeReload(config, target=server.run, sockets=[config.bind_socket()])
    supervisor.run()


def openapi():
    from deepdiff import DeepDiff
    from saatja.app import app

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
    # Used for PyCharm debugger integration
    which = sys.argv[1]
    if which == "main":
        main()
    elif which == "openapi":
        openapi()
    else:
        raise Exception(f"No idea what {which} is.")
