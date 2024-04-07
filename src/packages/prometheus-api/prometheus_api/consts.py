from aws_meta_aggregator.consts import (
    AWS_AGGREGATOR_RESOURCE_DEFAULT_ALLOWLIST,
    AWS_AGGREGATOR_RESOURCE_TAG_DEFAULT_ALLOWLIST,
)

from prometheus_api.utils.environment import env

APPLICATION_LOG_LEVEL = env("LOG_LEVEL", "DEBUG")

APPLICATION_LOG_RENDERER = env("LOG_RENDERER", "console")

APPLICATION_PROMETHEUS_HOST = env(
    "HOST",
    "0.0.0.0",  # nosec # B104:hardcoded_bind_all_interfaces, by design
)
APPLICATION_PROMETHEUS_PORT = int(env("PORT", "8000"))

APPLICATION_PROMETHEUS_RESOURCE_LABEL_ALLOWLIST: list[str] = list(
    env(
        "RESOURCE_LABEL_ALLOWLIST",
        AWS_AGGREGATOR_RESOURCE_DEFAULT_ALLOWLIST,
    ).split(" ")
)

APPLICATION_PROMETHEUS_RESOURCE_TAG_LABEL_ALLOWLIST: list[str] = list(
    env(
        "RESOURCE_TAG_LABEL_ALLOWLIST",
        AWS_AGGREGATOR_RESOURCE_TAG_DEFAULT_ALLOWLIST,
    ).split(" ")
)
