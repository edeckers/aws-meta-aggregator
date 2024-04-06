from typing import Any
import boto3
from moto import mock_aws
import pytest

from aws_meta_aggregator.prometheus_printers import (
    PrometheusResourcePrinter,
    PrometheusTagsPrinter,
)
from aws_meta_aggregator.resources import Resources

resource_printer = PrometheusResourcePrinter()
tags_printer = PrometheusTagsPrinter()


@pytest.fixture
def rgta_boto() -> Any:
    rgta = boto3.client(
        "resourcegroupstaggingapi", region_name="eu-central-1", verify=False
    )

    return rgta


@mock_aws
def test_retrieve_resources(rgta_boto: Any) -> None:
    print(rgta_boto)
    resources_client = Resources(rgta_boto)

    resources = resources_client.retrieve_resources()

    for resource in resources:
        resource_printer.print(resource)
        tags_printer.print(resource.arn, resource.tags)

    # FIXME Add assertions
