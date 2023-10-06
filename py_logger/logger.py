import logging
from typing import Any

import structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper("iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.NOTSET),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=False,
)


class Logger:
    def __init__(self, logger) -> None:
        self.logger = logger
        self.context: dict[str, any] = {}

    def add_context(self, **new_values: Any):
        self.context.update(new_values)

    def debug(self, event: str | None = None, *args: Any, **kw: Any) -> None:
        self._combine_with_context(kw)
        self.logger.debug(event, *args, **kw)

    def info(self, event: str | None = None, *args: Any, **kw: Any) -> None:
        self._combine_with_context(kw)
        self.logger.info(event, *args, **kw)

    def warning(self, event: str | None = None, *args: Any, **kw: Any) -> None:
        self._combine_with_context(kw)
        self.logger.warning(event, *args, **kw)

    def error(self, event: str | None = None, *args: Any, **kw: Any) -> None:
        self._combine_with_context(kw)
        self.logger.error(event, *args, **kw)

    def critical(self, event: str | None = None, *args: Any, **kw: Any) -> None:
        self._combine_with_context(kw)
        self.logger.critical(event, *args, **kw)

    def _combine_with_context(self, values: dict[str, any]):
        values.update(self.context)
        return values.update(self.context)


logger = Logger(structlog.get_logger())
