import json
import logging
import sys
from typing import Any, Callable

import structlog
from structlog.types import EventDict, WrappedLogger

from prometheus_api.consts import APPLICATION_LOG_LEVEL_BOTO3, APPLICATION_LOG_RENDERER


class AWSCloudWatchLogsRenderer:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        serializer: Callable[..., str | bytes] = json.dumps,
        **dumps_kw: Any,
    ) -> None:
        dumps_kw.setdefault("default", structlog.processors._json_fallback_handler)
        self._dumps_kw = dumps_kw
        self._dumps = serializer

    def __call__(self, logger: WrappedLogger, name: str, event_dict: EventDict) -> str:
        return str(self._dumps(event_dict, **self._dumps_kw))


# This bootstrapper is mostly inspired by:
# https://github.com/kitchenita/python-logger-cloudwatch-structlog
def __bootstrap_application_logger() -> None:
    aws_cloudwatch_renderer: Callable[[WrappedLogger, str, EventDict], str] = (
        AWSCloudWatchLogsRenderer(
            callouts=["event"], serializer=json.dumps, sort_keys=False
        )
    )
    console_renderer: Callable[[WrappedLogger, str, EventDict], str] = (
        structlog.dev.ConsoleRenderer()
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            (
                aws_cloudwatch_renderer
                if APPLICATION_LOG_RENDERER == "cloudwatch"
                else console_renderer
            ),
        ],
        context_class=dict,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG,  # ED Set to lowest level possible, so downstream loggers can filter individually
        force=True,
    )
    logging.getLogger("botocore").setLevel(APPLICATION_LOG_LEVEL_BOTO3)
    logging.getLogger("boto3").setLevel(APPLICATION_LOG_LEVEL_BOTO3)


def __bootstrap_loggers() -> None:
    __bootstrap_application_logger()


def bootstrap() -> None:
    __bootstrap_loggers()
