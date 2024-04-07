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
    def get_all(
        self,
    ) -> Response:
        _logger.info(
            "Received metrics request",
        )

        resources_client = Resources(boto3.client("resourcegroupstaggingapi"))

        resources = resources_client.retrieve_resources()

        resource_printer = PrometheusResourcePrinter()
        tags_printer = PrometheusTagsPrinter()

        output = []
        for resource in resources:
            output.append(resource_printer.print(resource))

            output.append(tags_printer.print(resource.tags))

        _logger.info(
            "Finished metrics request",
        )

        return Response(content="\n".join(output), media_type="text/plain")