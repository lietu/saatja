import json
import logging
import sys
from os import environ
from uuid import uuid4

from loguru import logger

from saatja.settings import conf

LOG_LEVEL = logging.DEBUG
IS_GCLOUD = conf.GCLOUD_PROJECT is not None
DEFAULT_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
    "<level>{message}</level> "
    "{extra}"
)


def gcloud_serializer(message):
    """
    Serializer for tweaking log record so it can be parsed by Google Cloud
    """
    # https://github.com/Delgan/loguru/issues/203
    record = message.record
    severity = record["level"].name
    if severity == "EXCEPTION":
        severity = "CRITICAL"

    google_trace_id = record["extra"].pop("google_trace_id", None)

    log_data = {
        "severity": severity,
        "raw": record["message"],
        "message": record["message"] + " | " + str(record["extra"]),
        "extra": record["extra"],
        "time": record["time"],
    }
    if google_trace_id:
        log_data[
            "logging.googleapis.com/trace"
        ] = f"projects/{conf.GCLOUD_PROJECT}/traces/{google_trace_id}"

    serialized = json.dumps(log_data, default=str)
    print(serialized, file=sys.stderr)


async def gcloud_logging_middleware(request, call_next):
    """
    Injecting request_id and Google Trace ID to log entries for Google Cloud
    """
    context = {}
    if IS_GCLOUD:
        context["request_id"] = str(uuid4())
        trace_header = request.headers.get("X-Cloud-Trace-Context")
        if trace_header:
            context["google_trace_id"] = trace_header.split("/")[0]

    with logger.contextualize(**context):
        return await call_next(request)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def init_logging(logger_):
    """
    Set up logging handlers. Output format is applied based on running environment

    :param logger_: Logger instance
    """
    # https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
    # intercept everything at the root logger
    logging.root.handlers = [InterceptHandler(level=LOG_LEVEL)]

    # remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger_.remove()
    if IS_GCLOUD:
        logger_.add(gcloud_serializer, format="{message}", level=logging.INFO)
    else:
        logger_.add(
            sys.stdout,
            format=environ.get("LOGURU_FORMAT", DEFAULT_FORMAT),
            colorize=True,
            level=logging.DEBUG,
        )


init_logging(logger)
