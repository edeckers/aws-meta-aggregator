from typing import Callable

from aws_meta_aggregator.consts import (
    AWS_AGGREGATOR_RESOURCE_DEFAULT_ALLOWLIST,
    AWS_AGGREGATOR_RESOURCE_TAG_DEFAULT_ALLOWLIST,
)
from aws_meta_aggregator.costs import Cost
from aws_meta_aggregator.resources import Resource, ResourceTag

_AVAILABLE_RESOURCE_LABELS: dict[str, Callable[[Resource], str | None]] = {
    "arn": lambda resource: resource.arn,
    "account": lambda resource: resource.account,
    "id": lambda resource: resource.resource_id,
    "partition": lambda resource: resource.partition,
    "region": lambda resource: resource.region,
    "service": lambda resource: resource.service,
    "type": lambda resource: resource.resource_type,
}

_AVAILABLE_RESOURCE_TAG_LABELS: dict[str, Callable[[ResourceTag], str | None]] = {
    "arn": lambda tag: tag.arn,
    "account": lambda tag: tag.account,
    "id": lambda tag: tag.resource_id,
    "key": lambda tag: tag.key,
    "partition": lambda tag: tag.partition,
    "region": lambda tag: tag.region,
    "service": lambda tag: tag.service,
    "type": lambda tag: tag.resource_type,
    "value": lambda tag: tag.value,
}

_DEFAULT_ALLOWLIST = AWS_AGGREGATOR_RESOURCE_DEFAULT_ALLOWLIST.split(" ")
_DEFAULT_RESOURCE_TAG_ALLOWLIST = AWS_AGGREGATOR_RESOURCE_TAG_DEFAULT_ALLOWLIST.split(
    " "
)


class PrometheusResourcePrinter:  # pylint: disable=too-few-public-methods
    def __init__(self, allowlist: list[str] = _DEFAULT_ALLOWLIST) -> None:
        self.__allowlist = allowlist

    def print(self, resource: Resource) -> str:
        allowed_labels = _AVAILABLE_RESOURCE_LABELS.keys() & self.__allowlist

        labels = [
            f'{label}="{_AVAILABLE_RESOURCE_LABELS[label](resource)}"'
            for label in allowed_labels
        ]

        return "".join(
            [
                "resource{",
                ", ".join(labels),
                "} 1",
            ]
        )


class PrometheusTagsPrinter:  # pylint: disable=too-few-public-methods
    def __init__(self, allowlist: list[str] = _DEFAULT_RESOURCE_TAG_ALLOWLIST) -> None:
        self.__allowlist = allowlist

    def print(self, tags: list[ResourceTag]) -> str:
        allowed_labels = _AVAILABLE_RESOURCE_TAG_LABELS.keys() & self.__allowlist

        output = []
        for tag in tags:
            labels = [
                f'{label}="{_AVAILABLE_RESOURCE_TAG_LABELS[label](tag)}"'
                for label in allowed_labels
            ]

            output.append(
                "".join(
                    [
                        "resource_tag{",
                        ", ".join(labels),
                        "} 1",
                    ]
                )
            )

        return "\n".join(output)


class PrometheusCostPrinter:  # pylint: disable=too-few-public-methods
    def print(self, resource: Cost) -> str:
        return "".join(
            [
                "cost{",
                f'dimension="{resource.dimension}",',
                f'name="{resource.name}",',
                f'currency="{resource.currency}"',
                f"}} {resource.cost:.10f}",
            ]
        )
