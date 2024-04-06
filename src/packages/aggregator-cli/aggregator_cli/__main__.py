#!/usr/bin/env python3

import argparse
import dataclasses
import json
from typing import Callable

import boto3

from aws_meta_aggregator.printers.prometheus_printers import (
    PrometheusResourcePrinter,
    PrometheusTagsPrinter,
)
from aws_meta_aggregator.resources import Resource, Resources, ResourceTag

__parser = argparse.ArgumentParser(
    prog="AWS Meta CLI", description="Access AWS resource information through CLI"
)


__command_subparsers = __parser.add_subparsers(help="commands", dest="command")

__resources_parser = __command_subparsers.add_parser(
    name="list-resources",
    add_help=True,
    help="List resources in a given format",
)

__resources_parser.add_argument("-f", "--format", type=str, required=True)


def __json_resource_printer(resource: Resource) -> None:
    print(json.dumps(dataclasses.asdict(resource)))


def __json_tags_printer(
    arn: str, tags: list[ResourceTag]  # pylint: disable=unused-argument
) -> None:
    pass


def __list_resources(arguments: argparse.Namespace) -> None:

    if not arguments.format in ["json", "prometheus"]:
        raise ValueError(
            f"Unknown format '{arguments.format}', expected one of 'json' or 'prometheus'"
        )

    print_resource = (
        __json_resource_printer
        if arguments.format == "json"
        else PrometheusResourcePrinter().print
    )
    print_tags = (
        __json_tags_printer
        if arguments.format == "json"
        else PrometheusTagsPrinter().print
    )

    resources_client = Resources(boto3.client("resourcegroupstaggingapi"))

    resources = resources_client.retrieve_resources()

    for resource in resources:
        print(print_resource(resource))

        print(print_tags(resource.arn, resource.tags))


__map_commands_to_processors: dict[str, Callable[[argparse.Namespace], None]] = {
    "list-resources": __list_resources,
}


def __run_command(arguments: argparse.Namespace) -> None:
    if arguments.command not in __map_commands_to_processors:
        raise ValueError(f"Unknown command: {arguments.command}")

    __map_commands_to_processors[arguments.command](arguments)


if __name__ == "__main__":
    __run_command(__parser.parse_args())
