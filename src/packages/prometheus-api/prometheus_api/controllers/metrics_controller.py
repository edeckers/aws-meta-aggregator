import boto3
import structlog
from aws_meta_aggregator.printers.prometheus_printers import (
    PrometheusResourcePrinter,
    PrometheusTagsPrinter,
)
from aws_meta_aggregator.resources import Resources
from fastapi import Response

_logger = structlog.get_logger()


class MetricsController:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        resource_label_allowlist: list[str],
        resource_tag_label_allowlist: list[str],
    ) -> None:
        self.__resource_label_allowlist = resource_label_allowlist
        self.__resource_tag_label_allowlist = resource_tag_label_allowlist

    def get_all(
        self,
    ) -> Response:
        _logger.info(
            "Received metrics request",
        )

        resources_client = Resources(boto3.client("resourcegroupstaggingapi"))

        resources = resources_client.retrieve_resources()

        resource_printer = PrometheusResourcePrinter(
            allowlist=self.__resource_label_allowlist
        )
        tags_printer = PrometheusTagsPrinter(
            allowlist=self.__resource_tag_label_allowlist
        )

        output = []
        for resource in resources:
            output.append(resource_printer.print(resource))

            output.append(tags_printer.print(resource.tags))

        _logger.info(
            "Finished metrics request",
        )

        return Response(content="\n".join(output), media_type="text/plain")
