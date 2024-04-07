import uuid

from aws_meta_aggregator.printers.prometheus_printers import (
    PrometheusResourcePrinter,
    PrometheusTagsPrinter,
)
from aws_meta_aggregator.resources import ResourceTag

resource_printer = PrometheusResourcePrinter()
tags_printer = PrometheusTagsPrinter()


def _random_key() -> str:
    return uuid.uuid4().hex


def _random_value() -> str:
    return uuid.uuid4().hex


def test_building_from_arn_type_0_succeeds() -> None:
    # arrange
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:something-db06309ec8ce58bb"

    # act
    tag = ResourceTag.from_arn(example_arn, _random_key(), _random_value())

    # assert
    assert tag.account == "123456789012"
    assert tag.partition == "aws"
    assert tag.resource_id == "something-db06309ec8ce58bb"
    assert tag.service == "ec2"
    assert tag.region == "eu-central-1"
    assert tag.resource_type is None
    assert tag.arn == example_arn


def test_building_from_arn_type_1_succeeds() -> None:
    # arrange
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:subnet:subnet-db06309ec8ce58bb"

    # act
    tag = ResourceTag.from_arn(example_arn, _random_key(), _random_value())

    # assert
    assert tag.account == "123456789012"
    assert tag.partition == "aws"
    assert tag.resource_id == "subnet-db06309ec8ce58bb"
    assert tag.service == "ec2"
    assert tag.region == "eu-central-1"
    assert tag.resource_type == "subnet"
    assert tag.arn == example_arn


def test_building_from_arn_type_2_succeeds() -> None:
    # arrange
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:subnet/subnet-db06309ec8ce58bb"

    # act
    tag = ResourceTag.from_arn(example_arn, _random_key(), _random_value())

    # assert
    assert tag.account == "123456789012"
    assert tag.partition == "aws"
    assert tag.resource_id == "subnet-db06309ec8ce58bb"
    assert tag.service == "ec2"
    assert tag.region == "eu-central-1"
    assert tag.resource_type == "subnet"
    assert tag.arn == example_arn


def test_correct_keys_and_values_are_returned() -> None:
    # arrange
    example_arn = "arn:aws:ec2:eu-central-1:123456789012:subnet/subnet-db06309ec8ce58bb"

    tag_key = _random_key()
    tag_value = _random_value()

    # act
    tag = ResourceTag.from_arn(example_arn, tag_key, tag_value)

    # assert
    assert tag.key == tag_key
    assert tag.value == tag_value
