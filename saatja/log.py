import logging

from loguru import logger

LOG_LEVEL = logging.DEBUG


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        logger_opt = logger.opt(depth=7, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


logging.getLogger("fastapi").handlers = [InterceptHandler(level=LOG_LEVEL)]
logging.getLogger("uvicorn").handlers = [InterceptHandler(level=LOG_LEVEL)]
