from typing import Any

import boto3
import pytest
from moto import mock_aws

from aws_meta_aggregator.printers.prometheus_printers import (
    PrometheusResourcePrinter,
    PrometheusTagsPrinter,
)
from aws_meta_aggregator.resources import Resource, Resources

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
    resources_client = Resources(rgta_boto)

    resources = resources_client.retrieve_resources()

    for resource in resources:
        resource_printer.print(resource)
        tags_printer.print(resource.tags)

    # FIXME Add assertions


def test_building_from_arn_type_0_succeeds() -> None:
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:something-db06309ec8ce58bb"
    resource = Resource.from_arn(
        example_arn,
        [],
    )

    assert resource.account == "123456789012"
    assert resource.partition == "aws"
    assert resource.resource_id == "something-db06309ec8ce58bb"
    assert resource.service == "ec2"
    assert resource.region == "eu-central-1"
    assert resource.resource_type is None
    assert resource.arn == example_arn


def test_building_from_arn_type_1_succeeds() -> None:
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:subnet:subnet-db06309ec8ce58bb"
    resource = Resource.from_arn(
        example_arn,
        [],
    )

    assert resource.account == "123456789012"
    assert resource.partition == "aws"
    assert resource.resource_id == "subnet-db06309ec8ce58bb"
    assert resource.service == "ec2"
    assert resource.region == "eu-central-1"
    assert resource.resource_type == "subnet"
    assert resource.arn == example_arn


def test_building_from_arn_type_2_succeeds() -> None:
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:subnet/subnet-db06309ec8ce58bb"
    resource = Resource.from_arn(
        example_arn,
        [],
    )

    assert resource.account == "123456789012"
    assert resource.partition == "aws"
    assert resource.resource_id == "subnet-db06309ec8ce58bb"
    assert resource.service == "ec2"
    assert resource.region == "eu-central-1"
    assert resource.resource_type == "subnet"
    assert resource.arn == example_arn
