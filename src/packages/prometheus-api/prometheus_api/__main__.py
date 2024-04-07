import argparse

import structlog
import uvicorn

from prometheus_api.api import bootstrap_api
from prometheus_api.bootstrap import bootstrap
from prometheus_api.consts import (
    APPLICATION_PROMETHEUS_HOST,
    APPLICATION_PROMETHEUS_PORT,
    APPLICATION_PROMETHEUS_RESOURCE_LABEL_ALLOWLIST,
    APPLICATION_PROMETHEUS_RESOURCE_TAG_LABEL_ALLOWLIST,
)

_logger = structlog.get_logger()

__cli_parser = argparse.ArgumentParser(
    prog="Prometheus Api", description="CLI to configure and start Prometheus Api"
)


__command_subparsers = __cli_parser.add_subparsers(help="commands", dest="command")

__run_api_parser = __command_subparsers.add_parser(
    name="run-api",
    add_help=False,
    help="Start the Prometheus Api in uvicorn ASGI web server",
)

__run_api_parser.add_argument(
    "-h",
    "--host",
    type=str,
    required=False,
    default=APPLICATION_PROMETHEUS_HOST,
)
__run_api_parser.add_argument(
    "-p", "--port", type=int, required=False, default=APPLICATION_PROMETHEUS_PORT
)

__run_api_parser.add_argument(
    "-ra",
    "--resource-label-allowlist",
    type=str,
    required=False,
    default=" ".join(APPLICATION_PROMETHEUS_RESOURCE_LABEL_ALLOWLIST),
)

__run_api_parser.add_argument(
    "-rta",
    "--resource-tag-label-allowlist",
    type=str,
    required=False,
    default=" ".join(APPLICATION_PROMETHEUS_RESOURCE_TAG_LABEL_ALLOWLIST),
)


def __run_api(arguments: argparse.Namespace) -> None:
    _logger.info(
        "Starting Prometheus Api",
        {
            "host": arguments.host,
            "port": arguments.port,
            "resource_label_allowlist": arguments.resource_label_allowlist,
            "resource_tag_label_allowlist": arguments.resource_tag_label_allowlist,
        },
    )

    api = bootstrap_api(
        resource_label_allowlist=arguments.resource_label_allowlist.split(" "),
        resource_tag_label_allowlist=arguments.resource_tag_label_allowlist.split(" "),
    )

    uvicorn.run(
        api,
        host=arguments.host,
        port=arguments.port,
    )


def __run_command(arguments: argparse.Namespace) -> None:
    bootstrap()

    if arguments.command == "run-api":
        __run_api(arguments)
        return

    raise ValueError(f"Unknown command: {arguments.command}")


if __name__ == "__main__":
    __run_command(__cli_parser.parse_args())
